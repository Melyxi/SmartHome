from core.extensions import client_mqtt


async def shutdown_mqtt(app):
    client_mqtt.disconnect()
