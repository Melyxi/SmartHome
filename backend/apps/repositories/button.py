from core.models.button import Button
from core.models.meta_button import MetaButton
from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository


class ButtonSqlAlchemyRepository(AsyncSqlAlchemyRepository[Button]):
    pass


class MetaButtonSqlAlchemyRepository(AsyncSqlAlchemyRepository[MetaButton]):
    pass
