import asyncio

from backend.core.adapter.transmitter_interface import ClientInterface


class ClientTransmitter(ClientInterface):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.writer = None
        self.reader = None  # Добавляем reader, если понадобится получать ответы

    async def connect(self):
        """Устанавливает соединение с сервером"""
        if self.writer is None:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            print(f"Соединение установлено с {self.host}:{self.port}")
        else:
            print("Соединение уже установлено")
        return self.writer

    async def send(self, message):
        """Отправляет сообщение на сервер"""
        if self.writer is None:
            raise RuntimeError("Сначала необходимо установить соединение с помощью метода connect()")

        # Преобразуем сообщение в байты и добавляем перевод строки (если нужно)
        if isinstance(message, str):
            message = message.encode()
        elif isinstance(message, bytes):
            message = message
        else:
            raise ValueError("Сообщение должно быть строкой или байтами")
        if message != b"":
            self.writer.write(message)
            await self.writer.drain()
            print(f"Отправлено: {message.decode().strip()}")

    async def close(self):
        """Закрывает соединение"""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            print("Соединение закрыто")
        else:
            print("Соединение уже закрыто")


# Создаем глобальный экземпляр клиента
client_instance: ClientTransmitter | None = None


async def initialize_client(host, port):
    global client_instance
    if client_instance is None:
        client_instance = ClientTransmitter(host, port)
        await client_instance.connect()
    else:
        print("Клиент уже инициализирован")


# Закрываем соединение при завершении работы
async def shutdown_client():
    if client_instance:
        await client_instance.close()


# Пример использования
if __name__ == "__main__":
    asyncio.run(initialize_client("127.0.0.1", 8888))

    async def main():
        await client_instance.send(b"Hello")

    asyncio.run(main())
