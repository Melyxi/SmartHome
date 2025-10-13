import asyncio
from collections import deque

import gmqtt
from core.configurate_logging import get_logger

server_logger = get_logger("server")


class AsyncClientZigbeeMQTT:
    topic_functions = {}
    messages = deque(maxlen=100)

    def __init__(self, host, port=1883, username: str | None = None, password: str | None = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client: gmqtt.Client | None = None
        self._task = None
        self._is_connected: bool = False

    @classmethod
    async def message_callback_add(cls, topic: str, function):
        cls.topic_functions[topic] = function
        print(f"Callback added for topic: {topic}")

    @classmethod
    async def message_callback_remove(cls, topic: str):
        if topic in cls.topic_functions:
            del cls.topic_functions[topic]
            print(f"Callback removed for topic: {topic}")

    def on_connect(self, client, flags, rc, properties):
        server_logger.info("[CONNECTED {}]", client._client_id)

        if self.topic_functions:
            for topic in self.topic_functions:
                client.subscribe(topic, qos=1)

        client.subscribe("zigbee2mqtt/#", qos=1)
        print("Subscribed to zigbee2mqtt/#")

    async def on_message(self, client, topic, payload, qos, properties):
        if payload and (message_function := self.topic_functions.get(topic)):
            await message_function(topic, payload, self.client)

        self.messages.append({topic: payload})
        server_logger.info(
            "[RECV MSG {}] TOPIC: {} PAYLOAD: {} QOS: {} PROPERTIES: {}",
            client._client_id,
            topic,
            payload,
            qos,
            properties,
        )

    @staticmethod
    def on_disconnect(client, packet, exc=None):
        server_logger.info("[DISCONNECTED {}]", client._client_id)

    @staticmethod
    def on_subscribe(client, mid, qos, properties):
        server_logger.info("[SUBSCRIBED {}] QOS: {}", client._client_id, qos)

    def assign_callbacks_to_client(self, client):
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect
        client.on_subscribe = self.on_subscribe

    async def listen_mqtt(self):
        while True:
            try:
                self.client = gmqtt.Client("zigbee-client")

                if self.username and self.password:
                    self.client.set_auth_credentials(self.username, self.password)

                self.assign_callbacks_to_client(self.client)

                await self.client.connect(self.host, self.port, keepalive=60)
                print("Connecting.....")
                break
            except Exception as e:
                self._is_connected = False
                server_logger.error(f"MQTT connection error: {e}")
                await asyncio.sleep(5)

    async def connect(self):
        """Запускает MQTT клиент"""
        self._task = asyncio.create_task(self.listen_mqtt())

    async def disconnect(self):
        """Останавливает MQTT клиент"""

        if self.client:
            await self.client.disconnect()
            self._is_connected = False
            print("MQTT listener stopped")

        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                print("MQTT listener stopped")
            except Exception as e:
                print(f"Error while disconnecting: {e}")
