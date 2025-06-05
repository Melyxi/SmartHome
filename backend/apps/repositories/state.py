from core.models.state import State
from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository


class StateSqlAlchemyRepository(AsyncSqlAlchemyRepository[State]):
    pass
