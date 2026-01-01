from core.cache.base.backend import BaseCache


class SceneCacheManager:
    scene_topic = "scene_"

    def __init__(self, cache: BaseCache):
        self.cache = cache

    async def set(self, key: str, cache_data: dict):
        cache_data.pop("linkquality", None)
        cache_data.pop("color_mode", None)
        # cache_data.pop("color", None)

        device_key = f"{self.scene_topic}{key}"
        await self.cache.delete(device_key)
        await self.cache.set(device_key, cache_data)

    async def get(self, key: str) -> dict:
        return await self.cache.get(f"{self.scene_topic}{key}")
