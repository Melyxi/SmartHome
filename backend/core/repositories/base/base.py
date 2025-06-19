from abc import ABC, abstractmethod
from typing import Generic, List, get_args

from core.extensions import db
from core.repositories.types import T


class SqlRepositoryAbstract(ABC, Generic[T]):
    model_cls: type[db.Base] | None = None

    def __init__(self, session):
        self.session = session

    def __init_subclass__(cls) -> None:
        cls.model_cls = get_args(
            cls.__orig_bases__[0]  # type: ignore  # pylint: disable=no-member
        )[0]

    @abstractmethod
    async def get_by_id(self, _id: int):
        return NotImplementedError

    @abstractmethod
    async def get_all(self):
        return NotImplementedError

    @abstractmethod
    async def get_by_filter(self, **kwargs):
        return NotImplementedError

    @abstractmethod
    async def create(self, **kwargs):
        return NotImplementedError

    @abstractmethod
    async def update(self, _id: int, **kwargs):
        return NotImplementedError

    @abstractmethod
    async def delete(self, _id: int):
        return NotImplementedError

    @abstractmethod
    async def bulk_delete(self, ids: List[int]):
        return NotImplementedError

    @abstractmethod
    async def bulk_create(self, **kwargs):
        return NotImplementedError

    @abstractmethod
    async def bulk_update(self, **kwargs):
        return NotImplementedError
