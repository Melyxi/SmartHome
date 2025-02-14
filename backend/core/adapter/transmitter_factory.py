from backend.core.adapter.transmitter import ClientTransmitter


class TransmitterFactory:
    _instance = None

    @classmethod
    async def get_client(cls, host: str, port: int):
        if cls._instance is None:
            cls._instance = ClientTransmitter(host, port)
            await cls._instance.connect()
        return cls._instance
