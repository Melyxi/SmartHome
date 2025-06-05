from configs.config import settings
from core.adapter.mqtt_client.client import AsyncClientZigbeeMQTT

client_mqtt = AsyncClientZigbeeMQTT(settings.get("MQTT_HOST"), settings.get("MQTT_PORT"))
async def startup_mqtt(app):
    await client_mqtt.connect()
    app.state.mqtt_client = client_mqtt


async def shutdown_mqtt(app):
    await client_mqtt.disconnect()
