from apps.domain.exceptions import ButtonsNotFoundValidationError, DevicesNotFoundValidationError
from apps.repositories.button import ButtonSqlAlchemyRepository
from apps.repositories.device import DeviceSqlAlchemyRepository
from core.extensions import db
from core.models.button import Button
from core.models.device import Device


async def populate_buttons(button_ids: list[int] | None) -> list[Button] | None:
    buttons: list[Button] = []
    if button_ids:
        async with db.async_session() as session:
            buttons = await ButtonSqlAlchemyRepository(session).get_by_ids(button_ids)

        if len(button_ids) != len(buttons):
            raise ButtonsNotFoundValidationError
    return buttons

async def populate_devices(device_ids: list[int] | None) -> list[Device] | None:
    devices: list[Button] = []
    if device_ids:
        async with db.async_session() as session:
            devices = await DeviceSqlAlchemyRepository(session).get_by_ids(device_ids)

        if len(device_ids) != len(devices):
            raise DevicesNotFoundValidationError
    return devices
