from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository
from core.models.state import State


class StateSqlAlchemyRepository(AsyncSqlAlchemyRepository[State]):
    pass
