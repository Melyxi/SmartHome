import uuid
from datetime import datetime
from pathlib import Path

from asyncpg.exceptions import UniqueViolationError
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError

from apps.domain.utils import populate_devices
from apps.models.scene import GetScene, PostScene, PostSceneWithCode
from configs.config import settings
from core.repositories.base.decorators import validate_db_error
from core.services.base.service import BaseService
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi


class SceneService(BaseService):
    get_model = GetScene

    async def list_scenes(self):
        scenes = await self.repository.get_all()
        response = []
        for scene in scenes:
            response.append(self.get_model.model_validate(scene, from_attributes=True))
        return response, 200

    async def get_scene(self, _id: int):
        scene = await self.repository.get_by_id(_id)
        response = self.get_model.model_validate(scene, from_attributes=True)
        return response, 200

    @validate_db_error
    async def create(self, scene: PostScene):
        self._properties = scene.model_dump()
        await self.validate_create()
        scene = await self.repository.create(**self._properties)
        return {"scene": scene.id}, 201

    @validate_db_error
    async def create_with_code(self, scene: PostSceneWithCode):
        self._properties = scene.model_dump()
        await self.validate_create_with_code()
        scene = await self.repository.create(**self._properties)
        return {"scene": scene.id}, 201

    async def __upload_file(self, file: UploadFile):
        file_content = await file.read()
        with open(Path(settings.BASE_DIR, settings.MEDIA_ROOT,
                        settings.UPLOAD_SCENE_DIR, file.filename), "wb") as f:
            f.write(file_content)
        relevant_path = Path(settings.UPLOAD_SCENE_DIR, file.filename)
        return str(relevant_path)


    async def validate_create(self):
        self._properties["devices"] = await populate_devices(self._properties["devices"])
        relevant_path = await self.__upload_file(self._properties["scene"])
        self._properties["scene"] = relevant_path



    async def __save_code_in_file(self, code: str):
        file_name = f"scene_{uuid.uuid4()}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"

        with open(Path(settings.BASE_DIR, settings.MEDIA_ROOT, settings.UPLOAD_SCENE_DIR, file_name), "w") as file:
            file.write(code)

        return str(Path(settings.UPLOAD_SCENE_DIR, file_name))



    async def validate_create_with_code(self):
        self._properties["devices"] = await populate_devices(self._properties["devices"])
        relevant_path = await self.__save_code_in_file(self._properties["code"])
        del self._properties["code"]
        self._properties["scene"] = relevant_path


