from apps.domain.exceptions import ButtonsNotFoundValidationError
from apps.repositories.button import ButtonSqlAlchemyRepository
from core.extensions import db
from core.models.button import Button


async def populate_buttons(button_ids: list[int] | None) -> list[Button] | None:
    buttons: list[Button] = []
    if button_ids:
        async with db.async_session() as session:
            buttons = await ButtonSqlAlchemyRepository(session).get_by_ids(button_ids)

        if len(button_ids) != len(buttons):
            raise ButtonsNotFoundValidationError
    return buttons
