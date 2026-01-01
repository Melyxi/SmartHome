import ast
import asyncio
import re
from pathlib import Path
from time import sleep

import aiofiles
from aiokafka import AIOKafkaProducer
from apps.domain.mqtt.cache import MqttCacheManager
from apps.domain.mqtt.commands import MqttCommands
from apps.domain.scenes.cache import SceneCacheManager
from apps.repositories.device import DeviceSqlAlchemyRepository
from apps.repositories.scene import SceneSqlAlchemyRepository
from configs.config import settings
from core.configurate_logging import get_logger
from core.enums import ProtocolType
from core.models.scene import Scene
from extensions import cache, db
from extensions import cache as backend_cache
from utils import json

scene_logger = get_logger("scene")


class SceneProcess:
    def __init__(self, scene, device):
        self.scene = scene
        self.devices = device

    async def process(self):
        script = Path(settings.BASE_DIR, settings.MEDIA_ROOT, self.scene.scene)

        async with aiofiles.open(script, encoding="utf-8") as file:
            lines = await file.readlines()

        lines.insert(0, "await asyncio.sleep(0.01)\n")
        code = "    ".join(lines)

        # from adapters.notifications.telegram import TelegramNotification
        safe_globals = {
            "__builtins__": {},
            "devices": self.devices,
            "print": print,
            "sleep": sleep,
            "asyncio": asyncio,
            "list": list,
            # "telegram": TelegramNotification
        }

        try:
            wrapped_code = f"async def __dynamic_code():\n    {code}\n"
            exec(wrapped_code, safe_globals, safe_globals)
            await safe_globals["__dynamic_code"]()
        except Exception as e:
            print(f"Ошибка: {e}")
            raise


class SceneFileManager:
    def __init__(self, scene: Scene):
        self.scene = scene

    @staticmethod
    async def get_targets(content):
        targets_pattern = r"targets\s*=\s*(\[.*?\])"
        targets_match = re.search(targets_pattern, content)
        targets = []
        if targets_match:
            targets = ast.literal_eval(targets_match.group(1))
        return targets

    @staticmethod
    async def get_receivers(content):
        receivers_pattern = r"receivers\s*=\s*(\[.*?\])"
        receivers_match = re.search(receivers_pattern, content)
        receivers = []
        if receivers_match:
            receivers = ast.literal_eval(receivers_match.group(1))
        return receivers

    async def get_file_content(self):
        async with aiofiles.open(Path(settings.BASE_DIR, settings.MEDIA_ROOT, self.scene.scene)) as file:
            content = await file.read()
        return content

    async def get_targets_and_receivers(self):
        content = await self.get_file_content()
        return await self.get_targets(content), await self.get_receivers(content)


class SceneManager:
    def __init__(self, device_name: str, client, message: dict | None = None):
        self.device_name = device_name
        self.client = client

        self.message = message
        if self.message is None:
            self.message = {}

    async def get_scenes_by_device(self):
        async with db.async_session() as session:
            scenes = await SceneSqlAlchemyRepository(session).get_scenes_with_device_by_unique_name(self.device_name)
        return scenes

    @staticmethod
    async def get_devices_by_names(names: list[str]):
        async with db.async_session() as session:
            devices = await DeviceSqlAlchemyRepository(session).get_devices_by_names(names)
        return devices

    async def _prepare_devices(self, scenes):
        map_scene_devices = {}

        for scene in scenes:
            _, receivers = await SceneFileManager(scene).get_targets_and_receivers()

            map_scene_devices[scene] = receivers
        all_device_names = set()
        for names in map_scene_devices.values():
            all_device_names.update(names)

        map_name_model_devices = {
            device.unique_name: device for device in await self.get_devices_by_names(list(all_device_names))
        }
        map_scene_devices = {
            scene: [map_name_model_devices[name] for name in names if name in map_name_model_devices]
            for scene, names in map_scene_devices.items()
        }
        return map_scene_devices

    async def prepare_device(self):
        scenes = await self.get_scenes_by_device()
        scene_map = {}
        map_scene_devices = await self._prepare_devices(scenes)

        for scene in scenes:
            device_map = {}

            for device in scene.devices + map_scene_devices[scene]:
                if device.unique_name == self.device_name:
                    device_command = DeviceCommand(device, self.client, self.message)
                else:
                    device_command = DeviceCommand(device, self.client, {})
                await device_command.set_property()
                device_map[device.unique_name] = device_command
            scene_map[scene] = device_map
        return scene_map

    async def process_scene(self):
        scenes = await self.prepare_device()
        for scene, devices in scenes.items():
            scene_logger.debug("Launch scene # {}", scene.id)
            await SceneProcess(scene, devices).process()


class DeviceCommand:
    def __init__(self, device, client, message: dict):
        self.device = device
        self.client = client
        self.message = message

    async def get_property_value(self):
        if self.message:
            return self.message

        return await MqttCacheManager(cache).get_one_record_by_device(self.device.unique_name)

    async def set_property(self):
        if hasattr(self.device, "exposes") and self.device.exposes:
            last_record = await self.get_property_value()
            protocol_type = self.device.protocol.type
            for expose in json.loads(self.device.exposes):
                expose_property = expose.get("property")
                if expose_property:
                    property_device = factory_type_device.get(protocol_type)(
                        property=expose_property,
                        value=last_record.get(expose_property),
                        device_name=self.device.unique_name,
                        client=self.client,
                    )
                    setattr(self, expose_property, property_device)
                else:
                    features = expose.get("features")
                    if features:
                        for feature in features:
                            expose_property = feature["property"]
                            property_device = factory_type_device.get(protocol_type)(
                                property=expose_property,
                                value=last_record.get(expose_property),
                                device_name=self.device.unique_name,
                                client=self.client,
                            )
                            setattr(self, expose_property, property_device)

    async def history(self, position=1):
        return await MqttCacheManager(cache).last_record(self.device.unique_name, position)

    async def set_cache(self, key: str, data: dict):
        cache_key = f"{self.device.uuid}_{key}"
        print(f"\n########{data=}########")
        await SceneCacheManager(backend_cache).set(cache_key, data)

    async def get_cache(self, key: str):
        cache_key = f"{self.device.uuid}_{key}"
        return await SceneCacheManager(backend_cache).get(cache_key)

    async def set(self, data: dict):
        protocol_type = self.device.protocol.type
        property_device = factory_type_device.get(protocol_type)(
            property=None, value=None, device_name=self.device.unique_name, client=self.client
        )
        await property_device.set(data)


class PropertyModule:
    def __init__(self, property: str | None, value: str | int | None, device_name: str, **kwargs):
        self.property = property
        self.value = value
        self.device_name = device_name

    async def set(self, value):
        data = value if self.property is None else {self.property: value}

        message = json.dumps(data)
        producer = AIOKafkaProducer(
            bootstrap_servers=f"{settings.get('BROKER_HOST')}:{settings.get('BROKER_PORT')}", enable_idempotence=True
        )
        await producer.start()
        try:
            await producer.send_and_wait(f"custom_module_{self.device_name}", message.encode("utf-8"))
        finally:
            await producer.stop()

        scene_logger.debug("Use SET message to module with data {} by device {}", message, self.device_name)


class PropertyDevice:
    def __init__(self, property: str, value: str | int | None, device_name: str, client, **kwargs):
        self.property = property
        self.value = value
        self.device_name = device_name
        self.client = client

    async def set(self, value):
        data = value if self.property is None else {self.property: value}

        await MqttCommands(self.client).set_data(self.device_name, data)
        scene_logger.debug("Use SET with data {} by device {}", json.dumps(data), self.device_name)


factory_type_device = {
    ProtocolType.MODULE: PropertyModule,
    ProtocolType.ZIGBEE: PropertyDevice,
}
