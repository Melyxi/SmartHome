from pathlib import Path
from time import sleep

from apps.domain.mqtt.cache import MqttCacheManager
from apps.domain.mqtt.commands import MqttCommands
from apps.repositories.scene import SceneSqlAlchemyRepository
from configs.config import settings
from core.extensions import cache, db
from utils import json

from core.configurate_logging import get_logger


scene_logger = get_logger("scene")

class SceneProcess:

    def __init__(self, scene, device):
        self.scene = scene
        self.devices = device

    async def process(self):
        script = Path(settings.BASE_DIR, settings.MEDIA_ROOT, self.scene.scene)

        with open(script, "r", encoding="utf-8") as file:
            lines = file.readlines()
        lines.insert(0, "sleep(3)\n")
        code = "    ".join(lines)

        safe_globals = {
            "__builtins__": {},
            "devices": self.devices,
            "print": print,
            "sleep": sleep
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
        scene_map = {}
        for scene in scenes:
            device_map = {}
            for device in scene.devices:
                device_command = DeviceCommand(device, self.client)
                await device_command.set_property()
                device_map[device.unique_name] = device_command
            scene_map[scene] = device_map
        return scene_map

    async def process_scene(self):
        scenes = await self.prepare_device()
        for scene, devices in scenes.items():
            scene_logger.debug("Launch scene # %s", scene.id)
            await SceneProcess(scene, devices).process()





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
                expose_property = expose.get("property")
                if expose_property:
                    property_device = PropertyDevice(expose_property,
                                                     last_record.get(expose_property),
                                                     self.device.unique_name, self.client)
                    setattr(self, expose_property, property_device)
                else:
                    features = expose.get("features")
                    if features:
                        for feature in features:
                            expose_property = feature["property"]
                            property_device = PropertyDevice(expose_property,
                                                             last_record.get(expose_property),
                                                             self.device.unique_name, self.client)
                            setattr(self, expose_property, property_device)


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
        scene_logger.debug("Use SET with data %s by device %s", json.dumps(data), self.device_name)
        await MqttCommands(self.client).set_data(self.device_name, data)


