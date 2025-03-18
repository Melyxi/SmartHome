from abc import ABC, abstractmethod


class ClientInterface(ABC):
    @abstractmethod
    async def connect(self):
        """Устанавливает соединение с сервером"""
        pass

    @abstractmethod
    async def send(self, message):
        """Отправляет сообщение на сервер"""
        pass

    @abstractmethod
    async def close(self):
        """Закрывает соединение"""
        pass
