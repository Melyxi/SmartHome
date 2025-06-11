from pathlib import Path

from apps.domain.mqtt.cache import MqttCacheManager
from apps.repositories.scene import SceneSqlAlchemyRepository
from configs.config import settings
from core.extensions import cache, db
from utils import json


class SceneProcess:

    def __init__(self, scene, device):
        self.scene = scene
        self.devices = device

    async def process(self):
        script = Path(settings.BASE_DIR, settings.MEDIA_ROOT, self.scene.scene)

        with open(script, "r", encoding="utf-8") as file:
            code = file.read()

        locals_dict = {
            "devices": self.devices,
        }

        try:
            exec(
                f"async def __dynamic_code():\n"
                f"    {code}\n",
                globals(),
                locals_dict
            )
            await locals_dict["__dynamic_code"]()  # Запускаем
        except Exception as e:
            raise e


class SceneManager:


    def __init__(self, device_name: str):
        self.device_name = device_name

    async def get_scenes_by_device(self):
        async with db.async_session() as session:
            scenes = await SceneSqlAlchemyRepository(session).get_scenes_with_device_by_unique_name(self.device_name)
        return scenes

    async def prepare_device(self):
        scenes = await self.get_scenes_by_device()
        for scene in scenes:
            device_map = {}
            for device in scene.devices:
                device_command = DeviceCommand(device)
                print(f'\n########{device_command=}########')
                await device_command.set_property()
                device_map[device.unique_name] = device_command

            await SceneProcess(scene, device_map).process()





class DeviceCommand:

    def __init__(self, device):
        self.device = device

    async def get_property_value(self):
        return await MqttCacheManager(cache).get_one_record_by_device(self.device.unique_name)

    async def set_property(self):
        if hasattr(self.device, "exposes") and self.device.exposes:
            last_record = await self.get_property_value()
            for expose in json.loads(self.device.exposes):
                expose_property = expose["property"]
                property_device = PropertyDevice(expose_property,  last_record.get(expose_property))
                setattr(self, expose["property"], property_device)


class PropertyDevice:

    def __init__(self, property, value):
        self.property = property
        self.value = value




