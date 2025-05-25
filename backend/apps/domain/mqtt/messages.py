from pathlib import Path

from apps.models.device import GetShortDevice
from apps.repositories.device import DeviceSqlAlchemyRepository
from configs.config import settings
from core.enums import ProtocolType
from core.extensions import client_mqtt, db
from core.models.device import Device
from core.models.protocol import Protocol
from core.templates import mqtt_device_html
from utils import json


def handle_mytopic(client, userdata, message):
    # client.subscribe("zigbee2mqtt/bridge/devices")
    client.subscribe("zigbee2mqtt/bridge/event")
    print(f'\n########{"decowwwwrator"=}########')
    client.subscribe("zigbee2mqtt/bridge/devices")
    print(f'\n########{client=}########')
    print(f'\n########{userdata=}########')
    print(f'\n########{message=}########')

client_mqtt.mqtt_client.message_callback_add("zigbee2mqtt/bridge/response/permit_join", handle_mytopic)


def bridge_event(client, userdata, message):
    print("event")
    print(f'\n########{client=}########')
    print(f'\n########{userdata=}########')
    print(f'\n########{message=}########')


client_mqtt.mqtt_client.message_callback_add("zigbee2mqtt/bridge/response/event", bridge_event)


def devices(client, userdata, message):
    print("devices")
    print(f'\n########{client=}########')
    print(f'\n########{userdata=}########')
    print(f'\n########{message=}########')
    msg_json = json.loads(message.payload)

    with open(Path(settings.BASE_DIR, "zigbee-devices.json"), "w+", encoding="utf-8") as f:
        json.dump(msg_json, f)

    zigbee_devices = [device for device in msg_json if device.get("type") == "EndDevice"]

    with db.sync_session() as session:
        existed_devices = session.query(Device).all()
    print(f'\n########{existed_devices=}########')

    existed_devices = [GetShortDevice.model_validate(device, from_attributes=True) for device in existed_devices]
    existed_devices_names = [device.unique_name for device in existed_devices]

    #
    # print(f'\n########{zigbee_devices=}########')

    zigbee_devices_dict = {device["ieee_address"]: device for device in zigbee_devices}

    different_devices = set(zigbee_devices_dict.keys())  - set(existed_devices_names)

    print(f'\n########{different_devices=}########')

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
        print(f'\n########{ieee_address=}########')
        client_mqtt.mqtt_client.subscribe(f"zigbee2mqtt/{ieee_address}")
        client_mqtt.mqtt_client.message_callback_add(f"zigbee2mqtt/{ieee_address}", message_from_device)

    # print(f'\n########{zigbee_devices_dict.keys()=}########')
    # print(f'\n########{existed_devices_names=}########')
    # print(f'\n########{existed_devices=}########')


    # print(f'\n########{msg_json=}########')


client_mqtt.mqtt_client.message_callback_add("zigbee2mqtt/bridge/devices", devices)


def message_from_device(client, userdata, message):
    json_message = json.loads(message.payload)

    topic = message.topic.split('/')[-1]
    result_msg = {topic: json_message}

    client_mqtt.messages.append(result_msg)

    # Добавить в кэш для истории

    print(f'\n########{message.payload=}########')
    print(f'\n########{message.topic=}########')
    print(f'\n########MESSAGE FROM DEVICES########')


