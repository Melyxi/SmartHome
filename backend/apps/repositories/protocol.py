from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository
from core.models.protocol import Protocol


class ProtocolSqlAlchemyRepository(AsyncSqlAlchemyRepository[Protocol]):
    pass
