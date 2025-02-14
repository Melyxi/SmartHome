from backend.core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository
from backend.core.models.protocol import Protocol


class ProtocolSqlAlchemyRepository(AsyncSqlAlchemyRepository[Protocol]):
    pass
