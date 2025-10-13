import asyncio
from pathlib import Path

from apps.domain.mqtt.cache import MqttCacheManager
from apps.domain.scenes.manager import SceneManager
from apps.models.device import GetShortDevice
from configs.config import settings
from core.adapter.mqtt_client.client import AsyncClientZigbeeMQTT
from core.configurate_logging import get_logger
from core.enums import ProtocolType
from core.extensions import cache, db
from core.models.device import Device
from core.models.protocol import Protocol
from core.templates import mqtt_device_html
from utils import json

scene_logger = get_logger("scene")


async def scene_run(device_name, client, message):
    scene_manager = SceneManager(device_name, client, message)
    await scene_manager.process_scene()


async def add_history_to_cache(device_name, json_message):
    mqtt_cache_manager = MqttCacheManager(cache)
    await mqtt_cache_manager.set_history_by_device(device_name, json_message)


background_tasks = set()


async def message_from_device(topic, message, client):
    json_message = json.loads(message)
    device_name = topic.split("/")[-1]

    scene_run_task = asyncio.create_task(scene_run(device_name, client, json_message))
    add_history_to_cache_task = asyncio.create_task(add_history_to_cache(device_name, json_message))

    background_tasks.add(scene_run_task)
    background_tasks.add(add_history_to_cache_task)

    scene_run_task.add_done_callback(background_tasks.discard)
    add_history_to_cache_task.add_done_callback(background_tasks.discard)

    scene_logger.debug(json_message)


async def devices(topic, message, client):
    msg_json = json.loads(message)
    with open(Path(settings.BASE_DIR, "zigbee-devices.json"), "w+", encoding="utf-8") as f:
        json.dump(msg_json, f)

    zigbee_devices = [device for device in msg_json if device.get("type") in ["EndDevice", "Router"]]

    with db.sync_session() as session:
        existed_devices = session.query(Device).all()

    existed_devices = [GetShortDevice.model_validate(device, from_attributes=True) for device in existed_devices]
    existed_devices_names = [device.unique_name for device in existed_devices]

    zigbee_devices_dict = {device["ieee_address"]: device for device in zigbee_devices}

    different_devices = set(zigbee_devices_dict.keys()) - set(existed_devices_names)

    new_devices = []
    protocol = None
    if different_devices:
        with db.sync_session() as session:
            protocol = session.query(Protocol).filter_by(type=ProtocolType.ZIGBEE.value).first()

    if protocol:
        for ieee_address in different_devices:
            new_device = {}
            zigbee_device = zigbee_devices_dict[ieee_address]
            new_device["unique_name"] = ieee_address
            new_device["name"] = zigbee_device["friendly_name"]
            new_device["description"] = zigbee_device["definition"]["description"]
            new_device["exposes"] = json.dumps(zigbee_device["definition"]["exposes"])
            new_device["protocol_id"] = protocol.id
            new_device["html"] = mqtt_device_html
            new_devices.append(new_device)

    with db.sync_session() as session:
        for device in new_devices:
            device_object = Device(**device)
            session.add(device_object)
            session.flush()

        session.commit()

    for ieee_address in zigbee_devices_dict:
        device_topic = f"zigbee2mqtt/{ieee_address}"
        await AsyncClientZigbeeMQTT.message_callback_add(device_topic, message_from_device)


router_message = {"zigbee2mqtt/bridge/devices": devices}
