import json

import aiofiles
from weather_api import EXPOSES_PATH


class ExposesManager:
    def get_exposes(self):
        with open(EXPOSES_PATH) as f:
            content = f.read()
            exposes = json.loads(content)
        return exposes

    async def async_get_exposes(self):
        async with aiofiles.open(EXPOSES_PATH, encoding="utf-8") as f:
            content = await f.read()
        return json.loads(content)

    async def serializer_exposes(self, data: dict, properties: dict):
        exposes = await self.async_get_exposes()

        temperature_display_mode = properties["temperature_display_mode"]
        result = {
            "temperature_display_mode": temperature_display_mode,
            "last_updated": data["current"]["last_updated"],
            "refresh_time": properties["refresh_time"],
        }
        for expose in exposes:
            name = expose["property"]
            if name == "current_temperature":
                if temperature_display_mode == "celsius":
                    result["current_temperature"] = data["current"]["temp_c"]
                else:
                    result["current_temperature"] = data["current"]["temp_f"]
            if name == "humidity":
                result["humidity"] = data["current"]["humidity"]

            if name == "city":
                result["city"] = data["location"]["name"]

        return result
