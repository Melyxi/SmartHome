import ast
import uuid
from datetime import datetime
from pathlib import Path

from asyncpg.exceptions import UniqueViolationError
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError

from apps.domain.exceptions import DevicesNotFoundValidationError
from apps.domain.scenes.exceptions import SceneNotFoundError, FileSyntaxError
from apps.domain.utils import populate_devices
from apps.models.scene import GetScene, PostScene, PostSceneWithCode, GetSceneWithCode, PatchScene
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
        if not scene:
            raise SceneNotFoundError
        response = self.get_model.model_validate(scene, from_attributes=True)
        return response, 200


    async def get_scene_with_code(self, _id: int):
        scene = await self.repository.get_by_id(_id)
        if not scene:
            raise SceneNotFoundError

        code = await self.__get_code_from_file(scene.scene)
        scene.code = code
        response = GetSceneWithCode.model_validate(scene, from_attributes=True)
        return response, 200


    @validate_db_error
    async def create(self, scene: PostScene):
        self._properties = scene.model_dump()
        await self.validate_create()
        scene = await self.repository.create(**self._properties)
        return {"scene": scene.id}, 201

    @validate_db_error
    async def update(self, _id: int, scene: PatchScene):
        self._properties = scene.model_dump(exclude_unset=True)
        self._model_id = _id
        await self.validate_update()
        print(f'\n########## {self._properties=} ##########')

    @validate_db_error
    async def create_with_code(self, scene: PostSceneWithCode):
        self._properties = scene.model_dump()
        await self.validate_create_with_code()
        scene = await self.repository.create(**self._properties)
        return {"scene": scene.id}, 201

    async def __upload_file(self, file: UploadFile):
        file_content = await file.read()

        await self.validate_with_ast(file_content.decode("utf-8"))

        filename = file.filename

        full_file_path = Path(settings.BASE_DIR, settings.MEDIA_ROOT,
                        settings.UPLOAD_SCENE_DIR, filename)

        if full_file_path.exists():


            full_file_path = Path(settings.BASE_DIR, settings.MEDIA_ROOT,
                                  settings.UPLOAD_SCENE_DIR, filename)

        with open(full_file_path, "wb") as f:
            f.write(file_content)
        relevant_path = Path(settings.UPLOAD_SCENE_DIR, filename)
        return str(relevant_path)


    async def validate_create(self):
        self._properties["devices"] = await populate_devices(self._properties["devices"])
        relevant_path = await self.__upload_file(self._properties["scene"])
        self._properties["scene"] = relevant_path


    async def __get_code_from_file(self, file_path: str):
        with open(Path(settings.BASE_DIR, settings.MEDIA_ROOT, file_path)) as f:
            code = f.read()
        return code


    async def __save_code_in_file(self, code: str):
        file_name = f"scene_{uuid.uuid4()}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"

        with open(Path(settings.BASE_DIR, settings.MEDIA_ROOT, settings.UPLOAD_SCENE_DIR, file_name), "w") as file:
            file.write(code)

        return str(Path(settings.UPLOAD_SCENE_DIR, file_name))


    async def validate_with_ast(self, code: str):
        try:
            ast.parse(code)
        except SyntaxError:
            raise FileSyntaxError


    async def validate_create_with_code(self):
        self._properties["devices"] = await populate_devices(self._properties["devices"])
        code = self._properties["code"]
        await self.validate_with_ast(code)

        relevant_path = await self.__save_code_in_file(code)
        del self._properties["code"]
        self._properties["scene"] = relevant_path

    async def __delete_file(self, path: str):
        file_path = Path(settings.BASE_DIR, settings.MEDIA_ROOT, path)
        file_path.unlink(missing_ok=True)


    async def __update_file(self, file: str):
        old_file = self._model.scene

        await self.__upload_file(file)
        await self.__delete_file(old_file)



    async def validate_update(self):

        # Validate model exists
        device_ids = self._properties.get("devices")
        scene = self._properties.get("scene")
        # Validate/Populate buttons
        try:
            if device_ids:
                buttons = await populate_devices(device_ids)
                self._properties["buttons"] = buttons
        except DevicesNotFoundValidationError:
            raise DevicesNotFoundValidationError


        if scene:
            old_file = self._model.scene
            await self.__upload_file(scene)
            await self.__delete_file(old_file)

