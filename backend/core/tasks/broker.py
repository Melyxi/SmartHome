from extensions import broker_producer


async def startup_broker_producer(app):
    await broker_producer.start()


async def shutdown_broker_producer(app):
    await broker_producer.stop()
