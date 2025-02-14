from backend.core.models.account import User
from backend.core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository


class AccountSqlAlchemyRepository(AsyncSqlAlchemyRepository[User]):
    pass
