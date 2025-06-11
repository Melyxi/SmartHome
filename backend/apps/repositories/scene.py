from core.models.device import Device
from core.models.scene import Scene
from core.repositories.base.sqlalchemy_repository import AsyncSqlAlchemyRepository
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class SceneSqlAlchemyRepository(AsyncSqlAlchemyRepository[Scene]):

    async def get_scenes_with_device_by_unique_name(self, device_unique_name: str, only_scene_fields: bool = False):
        query = select(Scene).join(Scene.devices).where(Device.unique_name == device_unique_name)

        if not only_scene_fields:
            query = query.options(selectinload(Scene.devices))

        result = await self.session.execute(query)
        return result.scalars().all()