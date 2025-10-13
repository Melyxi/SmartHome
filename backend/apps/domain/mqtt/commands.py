from gmqtt import Client
from utils import json


class MqttCommands:
    unacked_publish = set()

    def __init__(self, client: Client):
        self.client = client

    async def connect_devices(self, time=254):
        message = await self.client.publish("zigbee2mqtt/bridge/request/permit_join", f'{{"time": {time}}}', qos=1)
        return message

    async def disable_connect_devices(self):
        message = await self.client.publish("zigbee2mqtt/bridge/request/permit_join", '{"time": 0}', qos=1)
        return message

    async def bridge_event(self):
        message = await self.client.publish("zigbee2mqtt/bridge/event", '{"type":"device_interview"}', qos=1)
        return message

    async def devices(self):
        message = await self.client.publish("zigbee2mqtt/bridge/request/permit_join", "", qos=1)
        return message

    async def health_check(self):
        message = await self.client.publish("zigbee2mqtt/bridge/request/health_check", "", qos=1)
        return message

    async def info(self):
        message = await self.client.publish("zigbee2mqtt/bridge/info", "", qos=1)
        return message

    async def set_data(self, device_name: str, data: dict):
        message = self.client.publish(f"zigbee2mqtt/{device_name}/set", json.dumps(data).encode("utf-8"), qos=1)
        return message
