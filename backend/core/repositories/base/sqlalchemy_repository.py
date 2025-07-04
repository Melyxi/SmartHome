from typing import List

from core.repositories.base.base import SqlRepositoryAbstract
from core.repositories.base.exceptions import ModelNotFoundError
from core.repositories.types import T
from sqlalchemy import select


class AsyncSqlAlchemyRepository(SqlRepositoryAbstract[T]):
    async def get_by_id(self, _id: int) -> T | None:
        result = await self.session.execute(select(self.model_cls).filter_by(id=_id))
        return result.scalars().first()

    async def get_by_ids(self, _ids: list[int]) -> list[T]:
        result = await self.session.execute(select(self.model_cls).filter(self.model_cls.id.in_(_ids)))
        return result.scalars().all()

    async def get_all(self) -> list[T]:
        result = await self.session.execute(select(self.model_cls))
        return result.scalars().all()

    async def get_by_filter(self, **kwargs) -> list[T]:
        result = await self.session.execute(select(self.model_cls).filter_by(**kwargs))
        return result.scalars().all()


    async def create(self, **kwargs):
        async with self.session.begin():
            _object = self.model_cls(**kwargs)
            self.session.add(_object)
            await self.session.flush()
            await self.session.refresh(_object)
            return _object

    async def update(self, _id: int, **kwargs):
        _object = await self.get_by_id(_id)
        if not _object:
            raise ModelNotFoundError

        for key, value in kwargs.items():
            setattr(_object, key, value)

        self.session.add(_object)
        await self.session.flush()
        await self.session.refresh(_object)
        return _object

    async def delete(self, _id: int):
        _object = await self.get_by_id(_id)
        await self.session.delete(_object)
        await self.session.commit()

    async def bulk_delete(self, ids: List[int]):
        return None

    async def bulk_create(self):
        return None

    async def bulk_update(self):
        return None
