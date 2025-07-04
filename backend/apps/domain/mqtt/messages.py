from pathlib import Path

from apps.domain.mqtt.cache import MqttCacheManager
from apps.domain.scenes.manager import SceneManager
from apps.models.device import GetShortDevice
from configs.config import settings
from core.adapter.mqtt_client.client import AsyncClientZigbeeMQTT
from core.enums import ProtocolType
from core.extensions import cache, db
from core.models.device import Device
from core.models.protocol import Protocol
from core.templates import mqtt_device_html
from utils import json
from core.configurate_logging import get_logger

scene_logger = get_logger("scene")

async def message_from_device(message, client):
    json_message = json.loads(message.payload)
    device_name = message.topic.value.split('/')[-1]
    scene_logger.debug(json_message)
    mqtt_cache_manager = MqttCacheManager(cache)
    await mqtt_cache_manager.set_history_by_device(device_name, json_message)
    scene_manager = SceneManager(device_name, client)

    await scene_manager.process_scene()


async def devices(message, client):
    msg_json = json.loads(message.payload)
    with open(Path(settings.BASE_DIR, "zigbee-devices.json"), "w+", encoding="utf-8") as f:
        json.dump(msg_json, f)

    zigbee_devices = [device for device in msg_json if device.get("type") == "EndDevice"]

    with db.sync_session() as session:
        existed_devices = session.query(Device).all()

    existed_devices = [GetShortDevice.model_validate(device, from_attributes=True) for device in existed_devices]
    existed_devices_names = [device.unique_name for device in existed_devices]

    zigbee_devices_dict = {device["ieee_address"]: device for device in zigbee_devices}

    different_devices = set(zigbee_devices_dict.keys())  - set(existed_devices_names)

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
        await AsyncClientZigbeeMQTT.message_callback_add(f"zigbee2mqtt/{ieee_address}", message_from_device)


router_message = {"zigbee2mqtt/bridge/devices": devices}

