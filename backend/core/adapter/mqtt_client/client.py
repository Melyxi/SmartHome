import asyncio
from collections import deque

from aiomqtt import Client
from core.configurate_logging import get_logger

server_logger = get_logger("server")



class AsyncClientZigbeeMQTT:

    topic_functions = {}
    messages = deque(maxlen=100)
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
        self._task = None

    @classmethod
    async def message_callback_add(cls, topic: str, function):
        cls.topic_functions.update({topic: function})

    @classmethod
    async def message_callback_remove(cls, topic: str, function):
        if topic in cls.topic_functions:
            del cls.topic_functions[topic]

    async def on_message(self, message):
        if message_function := self.topic_functions.get(message.topic.value):
            await message_function(message)
        self.messages.append(message.payload.decode())

    async def listen_mqtt(self):
        while True:  # Бесконечный цикл для переподключения
            try:
                async with Client(self.host, self.port) as client:
                    print("MQTT is connected")
                    server_logger.info("MQTT is connected")

                    self.client = client
                    await client.subscribe("zigbee2mqtt/#")
                    async for message in client.messages:
                        await self.on_message(message)

            except Exception as e:
                print(f"MQTT connection error: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

    async def connect(self):
        self._task = asyncio.create_task(self.listen_mqtt())

    async def disconnect(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                print("MQTT listener stopped")
            except Exception as e:
                print(f"Error while disconnecting: {e}")
