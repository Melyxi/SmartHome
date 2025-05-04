from core.adapter.mqtt_client.commands import MqttCommands
from core.extensions import client_mqtt
from fastapi import APIRouter, WebSocket
from utils import json

mqtt_router = APIRouter()

@mqtt_router.get("/connect-device")
async def connect_devices():
    print(f'\n########{client_mqtt.messages=}########')
    mqtt_command = MqttCommands(client_mqtt.mqtt_client)
    mqtt_command.connect_devices()
    return {}

@mqtt_router.get("/disconnect-device")
async def disconnect_devices():
    print(f'\n########{client_mqtt.messages=}########')
    mqtt_command = MqttCommands(client_mqtt.mqtt_client)
    mqtt_command.connect_devices()
    return {}

# @client_mqtt.mqtt_client.message_callback()
# def recv_message(client, userdata, msg):
#     print(f'\n##########MESSAGES !!!!!!! ##########\n')

@mqtt_router.websocket("/mqtt")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            # data = json.loads(data)

            print(f'\n########{client_mqtt.messages=}########')

            # @client_mqtt.mqtt_client.message_callback()
            # def recv_message(client, userdata, msg):
            #     print(f'\n##########MESSAGES !!!!!!! ##########\n')

            print(f'\n########{data=}########')

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        print("Клиент отключился")

