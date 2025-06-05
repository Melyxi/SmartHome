from abc import ABC, abstractmethod
from typing import Any


class BaseCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    async def set(self, key: str, value: dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
