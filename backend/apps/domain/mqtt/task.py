from extensions import client_mqtt


async def startup_mqtt(app):
    await client_mqtt.connect()
    app.state.mqtt_client = client_mqtt


async def shutdown_mqtt(app):
    await client_mqtt.disconnect()
