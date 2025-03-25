from core.adapter.transmitter_interface import ClientInterface
from fastapi import Request, WebSocket


async def get_transmitter(websocket: WebSocket) -> ClientInterface:
    transmitter = getattr(websocket.app.state, "transmitter", None)
    if transmitter is None:
        raise RuntimeError("Transmitter не инициализирован. Убедитесь, что приложение запущено.")
    return transmitter
