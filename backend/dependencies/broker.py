from core.broker.kafka_producer import SmartHomeProducer
from extensions import broker_producer


async def get_kafka_producer() -> SmartHomeProducer:
    return broker_producer
