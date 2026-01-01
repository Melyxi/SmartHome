from uuid import UUID

from apps.models.device import DeviceExposesSchema
from core.models.button import Button
from core.models.device import Device
from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository
from sqlalchemy import select, union
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
            select(Device)
            .where(Device.id == _id)
            .options(
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
        uuids = []
        names_only = []
        for item in names:
            try:
                uuids.append(UUID(str(item)))
            except ValueError:
                names_only.append(item)
        unique_name_query = select(Device.id).where(Device.unique_name.in_(names_only))
        uuid_query = select(Device.id).where(Device.uuid.in_(uuids))

        union_query = union(unique_name_query, uuid_query).subquery()

        result = await self.session.execute(select(Device).where(Device.id.in_(select(union_query.c.id))).distinct())
        all_devices = result.scalars().all()
        return all_devices

    async def get_devices_expose_by_names(self, names: list[str]) -> list[DeviceExposesSchema]:
        result = await self.session.execute(
            select(Device.exposes, Device.unique_name).filter(Device.unique_name.in_(names))
        )
        return result.mappings().all()
