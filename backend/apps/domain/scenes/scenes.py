from apps.models.scene import GetScene
from core.services.base.service import BaseService


class SceneService(BaseService):
    get_model = GetScene

    async def list_scenes(self):
        scenes = await self.repository.get_all()
        response = []
        for scene in scenes:
            response.append(self.get_model.model_validate(scene, from_attributes=True))
        return response, 200
