from datetime import datetime, timezone

from core.cache.base.backend import BaseCache


class MqttCacheManager:
    device_topic = "device_"

    def __init__(self, cache: BaseCache):
        self.cache = cache

    async def get_one_record_by_device(self, device_name: str) -> dict:
        cache_data = await self.cache.get(f"{self.device_topic}{device_name}")
        cache_data = cache_data["history"]
        latest_timestamp = max(map(float, cache_data.keys()))
        latest_entry = cache_data[str(latest_timestamp)]
        return latest_entry

    async def get_history_by_device(self, device_name: str) -> dict:
        cache_data = await self.cache.get(f"{self.device_topic}{device_name}")

        return cache_data

    async def set_history_by_device(self, device_name: str, data: dict) -> None:
        utc_now = datetime.now(timezone.utc)
        timestamp = utc_now.timestamp()

        cache_data = await self.get_history_by_device(device_name)
        if cache_data is None:
            cache_data = {"history": {str(timestamp): data}}
        else:
            cache_data["history"][str(timestamp)] = data

        await self.cache.set(f"{self.device_topic}{device_name}", cache_data)
