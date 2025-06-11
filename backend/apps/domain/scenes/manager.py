from pathlib import Path

from apps.domain.mqtt.cache import MqttCacheManager
from apps.domain.mqtt.commands import MqttCommands
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
            lines = file.readlines()

        code = "    ".join(lines)

        safe_globals = {
            "__builtins__": {},
            "devices": self.devices,
            "print": print
        }

        try:
            wrapped_code = f"async def __dynamic_code():\n    {code}\n"
            exec(
                wrapped_code,
                safe_globals,
                safe_globals
            )
            await safe_globals["__dynamic_code"]()
        except Exception as e:
            print(f"Ошибка: {e}")
            raise


class SceneManager:


    def __init__(self, device_name: str, client):
        self.device_name = device_name
        self.client = client

    async def get_scenes_by_device(self):
        async with db.async_session() as session:
            scenes = await SceneSqlAlchemyRepository(session).get_scenes_with_device_by_unique_name(self.device_name)
        return scenes

    async def prepare_device(self):
        scenes = await self.get_scenes_by_device()
        for scene in scenes:
            device_map = {}
            for device in scene.devices:
                device_command = DeviceCommand(device, self.client)
                await device_command.set_property()
                device_map[device.unique_name] = device_command

            await SceneProcess(scene, device_map).process()





class DeviceCommand:

    def __init__(self, device, client):
        self.device = device
        self.client = client

    async def get_property_value(self):
        return await MqttCacheManager(cache).get_one_record_by_device(self.device.unique_name)

    async def set_property(self):
        if hasattr(self.device, "exposes") and self.device.exposes:
            last_record = await self.get_property_value()
            for expose in json.loads(self.device.exposes):
                expose_property = expose["property"]
                property_device = PropertyDevice(expose_property,
                                                 last_record.get(expose_property),
                                                 self.device.unique_name, self.client)
                setattr(self, expose["property"], property_device)


class PropertyDevice:

    def __init__(self, property: str, value: str | int | None, device_name: str, client):
        self.property = property
        self.value = value
        self.device_name = device_name
        self.client = client

    async def set(self, value):
        data = {
            self.property: value
        }

        await MqttCommands(self.client).set_data(self.device_name, data)


