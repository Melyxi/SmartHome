from core.models.button import Button
from core.models.device import Device
from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository
from sqlalchemy import select
from sqlalchemy.orm import subqueryload


class DeviceSqlAlchemyRepository(AsyncSqlAlchemyRepository[Device]):
    async def get_device_and_protocol_with_buttons_and_meta_with_states(self):
        result = await self.session.execute(
            select(Device).options(
                subqueryload(Device.protocol),
                subqueryload(Device.buttons).options(subqueryload(Button.meta_button), subqueryload(Button.states)),
            )
        )
        return result.scalars().all()

    async def get_device_and_protocol_with_buttons_and_meta_with_states_by_id(self, _id: int):
        result = await self.session.execute(
            select(Device).where(Device.id == _id).options(
                subqueryload(Device.protocol),
                subqueryload(Device.buttons).options(subqueryload(Button.meta_button), subqueryload(Button.states)),
            )
        )
        return result.scalars().first()

    async def get_with_button_by_id(self, _id: int):
        result = await self.session.execute(
            select(Device).options(
                subqueryload(Device.protocol),
                subqueryload(Device.buttons),
            )
        )
        return result.scalars().first()

    async def get_devices_by_names(self, names: list[str]) -> list[Device]:
        result = await self.session.execute(select(Device).filter(Device.unique_name.in_(names)))
        return result.scalars().all()