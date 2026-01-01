from core.adapter.mqtt_client.client import AsyncClientZigbeeMQTT
from fastapi import Request


async def get_mqtt_client(request: Request) -> AsyncClientZigbeeMQTT:
    return request.app.state.mqtt_client
