from adapters.broker.kafka_consumer import SmartHomeConsumer
from configs.config import settings

broker_consumer = SmartHomeConsumer(settings.get("BROKER_HOST"), settings.get("BROKER_PORT"))
