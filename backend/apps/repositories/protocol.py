from core.models.protocol import Protocol
from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository


class ProtocolSqlAlchemyRepository(AsyncSqlAlchemyRepository[Protocol]):
    pass
