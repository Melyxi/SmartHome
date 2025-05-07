from configs.config import settings
from core.adapter.mqtt_client.client import ClientZigbeeMQTT
from core.db.fastapi_asyncalchemy.base import SQLA

db = SQLA()

client_mqtt = ClientZigbeeMQTT(settings.get("MQTT_HOST"), settings.get("MQTT_PORT"))


