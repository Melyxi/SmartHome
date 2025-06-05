from core.models.scene import Scene
from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository


class SceneSqlAlchemyRepository(AsyncSqlAlchemyRepository[Scene]):
    pass