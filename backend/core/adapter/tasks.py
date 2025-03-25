from core.adapter.transmitter import ClientTransmitter
from configs.config import settings


async def startup_event(app):
    app.state.transmitter = ClientTransmitter(settings.get("TRANSMITTER_HOST"), settings.get("TRANSMITTER_PORT"))
    await app.state.transmitter.connect()
    print("Transmitter инициализирован")


async def shutdown_event(app):
    if hasattr(app.state, "transmitter"):
        await app.state.transmitter.close()
    print("Transmitter закрыт")
