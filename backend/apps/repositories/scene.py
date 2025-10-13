from core.models.device import Device
from core.models.scene import Scene
from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class SceneSqlAlchemyRepository(AsyncSqlAlchemyRepository[Scene]):

    async def get_scenes_with_device_by_unique_name(self, device_unique_name: str, only_scene_fields: bool = False)\
            -> list[Scene]:
        query = select(Scene).join(Scene.devices).where(Device.unique_name == device_unique_name, Scene.active == True)

        if not only_scene_fields:
            query = query.options(selectinload(Scene.devices))

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_scene_with_devices_by_id(self, _id: int, only_scene_fields: bool = False):
        query = select(Scene).where(Scene.id == _id)

        if not only_scene_fields:
            query = query.join(Scene.devices).options(selectinload(Scene.devices))

        result = await self.session.execute(query)
        return result.scalars().first()
