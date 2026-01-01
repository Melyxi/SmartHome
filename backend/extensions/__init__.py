from configs.config import settings
from core.adapter.mqtt_client.client import AsyncClientZigbeeMQTT
from core.broker.kafka_producer import SmartHomeProducer
from core.cache.mongodb.backend import MongoDBSCache
from core.db.fastapi_asyncalchemy.base import SQLA

db = SQLA()

cache = MongoDBSCache(settings.get("CACHE_URL"), settings.get("CACHE_TABLE"))

broker_producer = SmartHomeProducer(settings.get("BROKER_HOST"), settings.get("BROKER_PORT"))

client_mqtt = AsyncClientZigbeeMQTT(settings.get("MQTT_HOST"), settings.get("MQTT_PORT"))
