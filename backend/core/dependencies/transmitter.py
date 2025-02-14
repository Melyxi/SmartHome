from backend.core.adapter.transmitter_interface import ClientInterface
from fastapi import Request


async def get_transmitter(request: Request) -> ClientInterface:
    transmitter = getattr(request.app.state, "transmitter", None)
    if transmitter is None:
        raise RuntimeError("Transmitter не инициализирован. Убедитесь, что приложение запущено.")
    return transmitter
