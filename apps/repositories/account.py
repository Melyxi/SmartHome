from core.models.account import User
from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository


class AccountSqlAlchemyRepository(AsyncSqlAlchemyRepository[User]):
    pass
