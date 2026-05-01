from configs.config import settings
from core.adapter.transmitter import ClientTransmitter
from core.configurate_logging import get_logger

logger = get_logger("server")

async def startup_event(app):
    app.state.transmitter = ClientTransmitter(settings.get("TRANSMITTER_HOST"), settings.get("TRANSMITTER_PORT"))
    try:
        await app.state.transmitter.connect()
        logger.info("Transmitter is initialization")
    except ConnectionRefusedError as ex:
        print(f"Transmitter error: {ex}")


async def shutdown_event(app):
    if hasattr(app.state, "transmitter"):
        await app.state.transmitter.close()
    logger.info("Transmitter is closed")
