import asyncio

from core.adapter.mqtt_client.commands import MqttCommands
# from core.extensions import client_mqtt
from fastapi import APIRouter, WebSocket
from utils import json
from collections import deque

mqtt_router = APIRouter()

@mqtt_router.get("/connect-device")
async def connect_devices():
    # print(f'\n########{client_mqtt.messages=}########')
    # mqtt_command = MqttCommands(client_mqtt.mqtt_client)
    # mqtt_command.connect_devices()
    return {}

@mqtt_router.get("/disconnect-device")
async def disconnect_devices():
    # print(f'\n########{client_mqtt.messages=}########')
    # mqtt_command = MqttCommands(client_mqtt.mqtt_client)
    # mqtt_command.disable_connect_devices()
    return {}

@mqtt_router.get("/event")
async def bridge_event():
    # mqtt_command = MqttCommands(client_mqtt.mqtt_client)
    # mqtt_command.bridge_event()
    return {}


@mqtt_router.get("/zigbee-devices")
async def devices():
    # mqtt_command = MqttCommands(client_mqtt.mqtt_client)
    # mqtt_command.devices()
    return {}

# @client_mqtt.mqtt_client.message_callback()
# def recv_message(client, userdata, msg):
#     print(f'\n##########MESSAGES !!!!!!! ##########\n')


active_connections = []
states_connection: dict = {}


@mqtt_router.websocket("/mqtt")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    active_connections.append(websocket)

    print(f'\n########{active_connections=}########')
    try:
        print(f'\n########START########')
        while True:
            print(f'\n########START1########')



            # print(f'\n########{client_mqtt.messages=}########')

            # @client_mqtt.mqtt_client.message_callback()
            # def recv_message(client, userdata, msg):
            #     print(f'\n##########MESSAGES !!!!!!! ##########\n')

            # messages = client_mqtt.messages
            # client_mqtt.messages = deque(maxlen=100)

            # if messages:
            #     for msg in messages:
            #         print(f'\n########{msg=}########')
            #         for connection in active_connections:
            #             await connection.send_text(json.dumps(msg))

            await asyncio.sleep(0.01)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        active_connections.remove(websocket)  # Удаляем клиента из списка при отключении
        print("Клиент отключился")

