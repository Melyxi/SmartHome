import asyncio
import json
from json import JSONDecodeError
from typing import Any

import aiofiles
import niquests
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from exposes import ExposesManager
from schemas import ResponseCurrentWeatherSchema
from weather_api import JSON_FILE_PATH, UUID_FILE_PATH


class WeatherApiManager:
    # base_uri = "http://api.weatherapi.com/v1/current.json?key=6483ea5b5c8b42cc84d202625252111&q=London&aqi=no"
    base_uri = "http://api.weatherapi.com/v1/current.json?key="

    def __init__(self, app):
        self.app = app

        api_key = self.app.config.get("WEATHER_API_KEY")

        if not api_key:
            raise

        self.uri = f"{self.base_uri}{api_key}"

    async def response_weather(self, properties: dict):
        city = properties["city"]
        response = niquests.get(f"{self.uri}&q={city}&aqi=no")
        if 200 <= response.status_code <= 300:
            weather = ResponseCurrentWeatherSchema(**response.json())
            return weather.model_dump()


class MainWeatherManager:
    def __init__(self, app):
        self.app = app
        self.module_uuid = None

        self.set_uuid()

        self.consumer = AIOKafkaConsumer(
            bootstrap_servers=f"{self.app.config.get('BROKER_HOST')}:{self.app.config.get('BROKER_PORT')}",
        )

        self.api_manager = WeatherApiManager(self.app)
        self.exposes_manager = ExposesManager()

    def set_uuid(self):
        with open(UUID_FILE_PATH) as file:
            self.module_uuid = file.readline()

    @staticmethod
    async def get_property_from_json() -> dict[str, Any]:
        async with aiofiles.open(JSON_FILE_PATH, encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)

    async def update_properties(self, data: dict[str, Any]):
        json_str = json.dumps(data, ensure_ascii=False, indent=4)
        async with aiofiles.open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
            await f.write(json_str)

    async def set_message(self, message):
        producer = AIOKafkaProducer(
            bootstrap_servers=f"{self.app.config.get('BROKER_HOST')}:{self.app.config.get('BROKER_PORT')}",
            enable_idempotence=True,
        )
        await producer.start()
        try:
            await producer.send_and_wait(f"custom_module_set_{self.module_uuid}", json.dumps(message).encode("utf-8"))
        finally:
            await producer.stop()

    async def background_worker(self):
        await self.consumer.start()
        self.consumer.subscribe(pattern=f"custom_module_{self.module_uuid}*")

        properties = await self.get_property_from_json()
        initial_refresh_time = properties.get("refresh_time")

        while True:
            try:
                result = await self.consumer.getmany(timeout_ms=initial_refresh_time * 1000)
                for _, messages in result.items():
                    if messages:
                        for message in messages:
                            msg = message.value.decode("utf-8")
                            try:
                                msg = json.loads(msg)
                                properties = await self.get_property_from_json()

                                temperature_display_mode = msg.get("temperature_display_mode")
                                refresh_time = msg.get("refresh_time")
                                city = msg.get("city")

                                if temperature_display_mode or refresh_time or city:
                                    update_data = {}
                                    if temperature_display_mode:
                                        update_data["temperature_display_mode"] = temperature_display_mode
                                    if refresh_time:
                                        update_data["refresh_time"] = refresh_time
                                        initial_refresh_time = refresh_time
                                    if city:
                                        update_data["city"] = city

                                    if update_data:
                                        properties.update(update_data)
                                        await self.update_properties(properties)
                                    weather = await self.api_manager.response_weather(properties)
                                    if weather:
                                        send_data = await self.exposes_manager.serializer_exposes(weather, properties)
                                        await self.set_message(send_data)
                                    else:
                                        print("Status 400")
                            except (AttributeError, JSONDecodeError) as e:
                                print(f"Process message error: {e}")

                else:
                    # Ваша логика здесь
                    print("Background task is running...")

                    properties = await self.get_property_from_json()
                    weather = await self.api_manager.response_weather(properties)

                    if weather:
                        send_data = await self.exposes_manager.serializer_exposes(weather, properties)
                        await self.set_message(send_data)
                    else:
                        print("Status 400")

                    # Например, обновление данных каждые 30 секунд
                    # await asyncio.sleep(30)

            except Exception as e:
                print(f"Background task error: {e}")

                await asyncio.sleep(60)
