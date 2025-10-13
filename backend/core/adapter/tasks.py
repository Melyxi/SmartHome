from configs.config import settings
from core.adapter.transmitter import ClientTransmitter


async def startup_event(app):
    app.state.transmitter = ClientTransmitter(settings.get("TRANSMITTER_HOST"), settings.get("TRANSMITTER_PORT"))
    try:
        await app.state.transmitter.connect()
        print("Transmitter инициализирован")
    except ConnectionRefusedError as ex:
        print(ex)

async def shutdown_event(app):
    if hasattr(app.state, "transmitter"):
        await app.state.transmitter.close()
    print("Transmitter закрыт")
