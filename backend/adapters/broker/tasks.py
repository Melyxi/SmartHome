from core.configurate_logging import get_logger
from extensions.broker import broker_consumer
from fastapi import FastAPI

server_logger = get_logger("server")


async def startup_broker_consumer(app: FastAPI) -> None:
    await broker_consumer.start()
    server_logger.info("Kafka consumer started!")


async def shutdown_broker_consumer(app: FastAPI) -> None:
    await broker_consumer.stop()
    server_logger.info("Kafka consumer stopped!")
