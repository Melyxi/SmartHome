from typing import List

from sqlalchemy import select

from backend.core.repositories.base.base import SqlRepositoryAbstract
from core.repositories.types import T


class AsyncSqlAlchemyRepository(SqlRepositoryAbstract[T]):
    async def get_by_id(self, _id: int) -> T | None:
        result = await self.session.execute(select(self.model_cls).filter_by(id=_id))
        return result.scalars().first()

    async def get_all(self):
        result = await self.session.execute(select(self.model_cls))
        return result.scalars().all()

    async def get_by_filter(self, **kwargs):
        result = await self.session.execute(select(self.model_cls).filter_by(**kwargs))
        return result.scalars().all()

    async def create(self, **kwargs):
        _object = self.model_cls(**kwargs)
        self.session.add(_object)
        await self.session.commit()
        await self.session.refresh(_object)
        return _object

    async def update(self, _id: int, **kwargs):
        _object = await self.get_by_id(_id)
        for key, value in kwargs.items():
            setattr(_object, key, value)
        await self.session.commit()
        await self.session.refresh(_object)
        return _object

    async def delete(self, _id: int) -> bool:
        _object = await self.get_by_id(_id)
        self.session.delete(_object)
        return True

    async def bulk_delete(self, ids: List[int]):
        return None

    async def bulk_create(self):
        return None

    async def bulk_update(self):
        return None
