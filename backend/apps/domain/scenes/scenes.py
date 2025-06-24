import ast
import uuid
from datetime import datetime
from pathlib import Path

from apps.domain.exceptions import DevicesNotFoundValidationError
from apps.domain.scenes.exceptions import FileSyntaxError, SceneNotFoundError
from apps.domain.utils import populate_devices
from apps.models.device import ShortGetDevice
from apps.models.scene import (
    GetScene,
    GetSceneWithCode,
    GetSceneWithCodeWithDevices,
    GetSceneWithDevices,
    PatchScene,
    PatchSceneWithCode,
    PostScene,
    PostSceneWithCode,
)
from configs.config import settings
from core.repositories.base.decorators import validate_db_error
from core.repositories.base.exceptions import DatabaseValidateError, ModelNotFoundError
from core.services.base.service import BaseService
from core.utils.file import generate_unique_name
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError


class SceneService(BaseService):
    get_model = GetScene

    async def list_scenes(self):
        scenes = await self.repository.get_all()
        response = []
        for scene in scenes:
            response.append(self.get_model.model_validate(scene, from_attributes=True))
        return response, 200

    async def get_scene(self, _id: int):
        scene = await self.repository.get_scene_with_devices_by_id(_id)
        if not scene:
            raise SceneNotFoundError
        response = GetSceneWithDevices.model_validate(scene, from_attributes=True)
        return response, 200


    async def get_scene_with_code(self, _id: int):
        scene = await self.repository.get_scene_with_devices_by_id(_id)
        if not scene:
            raise SceneNotFoundError

        code = await self.__get_code_from_file(scene.scene)
        scene.code = code
        response = GetSceneWithCodeWithDevices.model_validate(scene, from_attributes=True)
        return response, 200

    @staticmethod
    async def _mixin_devices(model, scene, devices):
        scene_model = scene.model_dump()
        scene_model["devices"] = devices
        scene = model.model_validate(scene_model)
        return scene

    @validate_db_error
    async def create(self, scene: PostScene):
        self._properties = scene.model_dump()
        await self.validate_create()
        try:
            scene = await self.repository.create(**self._properties)
            devices = [ShortGetDevice.model_validate(device, from_attributes=True)
                       for device in self._properties["devices"]]
        except IntegrityError:
            await self.__delete_file(self._properties["scene"])
            raise

        scene = self.get_model.model_validate(scene, from_attributes=True)
        scene = await self._mixin_devices(GetSceneWithDevices, scene, devices)
        return scene, 201

    @validate_db_error
    async def update(self, _id: int, scene: PatchScene | PatchSceneWithCode, is_code: bool = False):
        async with self.repository.session.begin():
            self._properties = scene.model_dump(exclude_unset=True, exclude_none=True)
            self._model_id = _id
            await self.validate_update()
            code = self._properties.get("code")
            if code:
                del self._properties["code"]
            try:
                scene = await self.repository.update(self._model_id, **self._properties)
            except (IntegrityError, DatabaseValidateError):
                await self.__delete_file(self._properties["scene"])
                raise
            except ModelNotFoundError:
                await self.__delete_file(self._properties["scene"])
                raise SceneNotFoundError

            if is_code:
                scene.code = code
                scene = GetSceneWithCode.model_validate(scene, from_attributes=True)
            else:
                scene = self.get_model.model_validate(scene, from_attributes=True)

        return scene, 200

    @validate_db_error
    async def create_with_code(self, scene: PostSceneWithCode):
        self._properties = scene.model_dump()
        await self.validate_create_with_code()
        try:
            code = self._properties["code"]
            del self._properties["code"]

            scene = await self.repository.create(**self._properties)
            devices = [ShortGetDevice.model_validate(device, from_attributes=True)
                       for device in self._properties["devices"]]
            scene.code = code
        except IntegrityError:
            await self.__delete_file(self._properties["scene"])
            raise
        scene = GetSceneWithCode.model_validate(scene, from_attributes=True)
        scene = await self._mixin_devices(GetSceneWithCodeWithDevices, scene, devices)
        return scene, 201

    @staticmethod
    async def build_full_file_path(filename: str, is_relevant_path: bool = False) -> Path:

        if not is_relevant_path:
            full_file_path = Path(settings.BASE_DIR, settings.MEDIA_ROOT,
                                settings.UPLOAD_SCENE_DIR, filename)
        else:
            full_file_path = Path(settings.BASE_DIR, settings.MEDIA_ROOT, filename)

        return full_file_path

    async def __upload_file(self, file: UploadFile):
        file_content = await file.read()

        await self.validate_with_ast(file_content.decode("utf-8"))

        filename = file.filename
        full_file_path = await self.build_full_file_path(filename)

        if full_file_path.exists():
            filename = await generate_unique_name(filename)
            full_file_path = await self.build_full_file_path(filename)

        with open(full_file_path, "wb") as f:
            f.write(file_content)
        relevant_path = Path(settings.UPLOAD_SCENE_DIR, filename)
        return str(relevant_path)


    async def validate_create(self):
        self._properties["devices"] = await populate_devices(self._properties["devices"])
        relevant_path = await self.__upload_file(self._properties["scene"])
        self._properties["scene"] = relevant_path


    async def __get_code_from_file(self, file_path: str) -> str:
        with open(Path(settings.BASE_DIR, settings.MEDIA_ROOT, file_path)) as f:
            code = f.read()
        return code


    async def __save_code_in_file(self, code: str) -> str:
        file_name = f"scene_{uuid.uuid4()}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"

        full_file_path = await self.build_full_file_path(file_name)

        with open(full_file_path, "w") as file:
            file.write(code)

        return str(Path(settings.UPLOAD_SCENE_DIR, file_name))


    async def __update_code_in_file(self, code: str, relevant_path: str):
        full_file_path = await self.build_full_file_path(relevant_path, is_relevant_path=True)
        with open(full_file_path, "w") as file:
            file.write(code)


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

        self._properties["scene"] = relevant_path

    async def __delete_file(self, path: str):
        file_path = Path(settings.BASE_DIR, settings.MEDIA_ROOT, path)
        file_path.unlink(missing_ok=True)


    async def __update_file(self, file: UploadFile):
        old_file = self._model.scene
        scene = await self.__upload_file(file)
        self._properties["scene"] = scene
        await self.__delete_file(old_file)


    async def validate_update(self):
        # Validate model exists
        scene_model = await self.repository.get_by_id(self._model_id)

        if not scene_model:
            raise SceneNotFoundError

        self._model = scene_model

        device_ids = self._properties.get("devices")
        scene = self._properties.get("scene")
        code = self._properties.get("code")

        # Validate/Populate buttons
        try:
            if device_ids:
                buttons = await populate_devices(device_ids)
                self._properties["buttons"] = buttons
        except DevicesNotFoundValidationError:
            raise DevicesNotFoundValidationError

        if scene:
            await self.__update_file(scene)

        if code:
            await self.validate_with_ast(code)
            await self.__update_code_in_file(code, scene_model.scene)

    async def validate_delete(self):
        scene_model = await self.repository.get_by_id(self._model_id)

        if not scene_model:
            raise SceneNotFoundError
        self._model = scene_model

    async def delete(self, _id: int):
        self._model_id = _id
        async with self.repository.session.begin():
            await self.validate_delete()
            await self.repository.delete(self._model_id)

        await self.__delete_file(self._model.scene)
