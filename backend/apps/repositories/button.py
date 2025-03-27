from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository
from core.models.button import Button
from core.models.meta_button import MetaButton


class ButtonSqlAlchemyRepository(AsyncSqlAlchemyRepository[Button]):
    pass


class MetaButtonSqlAlchemyRepository(AsyncSqlAlchemyRepository[MetaButton]):
    pass
