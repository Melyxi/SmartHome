from backend.core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository
from backend.core.models.state import State


class StateSqlAlchemyRepository(AsyncSqlAlchemyRepository[State]):
    pass
