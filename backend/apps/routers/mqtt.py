import asyncio
from collections import deque
from typing import Annotated

from apps.domain.mqtt.commands import MqttCommands
from core.adapter.mqtt_client.client import AsyncClientZigbeeMQTT
from core.dependencies.mqtt import get_mqtt_client
from fastapi import APIRouter, Depends, WebSocket
from utils import json

mqtt_router = APIRouter()

@mqtt_router.get("/connect-device")
async def connect_devices(mqtt_client : Annotated[AsyncClientZigbeeMQTT, Depends(get_mqtt_client)]):
    mqtt_command = MqttCommands(mqtt_client.client)
    await mqtt_command.connect_devices()
    return {}


@mqtt_router.get("/disconnect-device")
async def disconnect_devices(mqtt_client : Annotated[AsyncClientZigbeeMQTT, Depends(get_mqtt_client)]):
    mqtt_command = MqttCommands(mqtt_client.client)
    await mqtt_command.disable_connect_devices()
    return {}

@mqtt_router.get("/event")
async def bridge_event(mqtt_client : Annotated[AsyncClientZigbeeMQTT, Depends(get_mqtt_client)]):
    mqtt_command = MqttCommands(mqtt_client.client)
    await mqtt_command.bridge_event()
    return {}


@mqtt_router.get("/zigbee-devices")
async def devices(mqtt_client : Annotated[AsyncClientZigbeeMQTT, Depends(get_mqtt_client)]):
    mqtt_command = MqttCommands(mqtt_client.client)
    await mqtt_command.devices()
    return {}


active_connections = []
states_connection: dict = {}


@mqtt_router.websocket("/mqtt")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    active_connections.append(websocket)
    try:
        while True:

            messages = AsyncClientZigbeeMQTT.messages
            AsyncClientZigbeeMQTT.messages = deque(maxlen=100)

            if messages:
                for msg in messages:
                    for connection in active_connections:
                        await connection.send_text(json.dumps(msg))

            await asyncio.sleep(0.01)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        active_connections.remove(websocket)  # Удаляем клиента из списка при отключении
        print("Клиент отключился")

