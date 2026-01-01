from aiokafka import AIOKafkaProducer
from core.configurate_logging import get_logger

server_logger = get_logger("server")


class SmartHomeProducer:
    def __init__(self, host: str = "localhost", port: str = "29092"):
        self.producer = AIOKafkaProducer(bootstrap_servers=f"{host}:{port}")

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_and_wait(self, topic: str, message: str):
        server_logger.debug("Topic: {}, message: {}", topic, message)
        await self.producer.send_and_wait(topic, message)
