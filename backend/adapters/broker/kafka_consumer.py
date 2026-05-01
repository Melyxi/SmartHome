import asyncio
import contextlib

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from apps.domain.mqtt.messages import add_history_to_cache, scene_run
from core.configurate_logging import get_logger
from extensions import client_mqtt
from utils import json

server_logger = get_logger("server")

background_tasks = set()


class SmartHomeConsumer:
    topic_prefix = ["mqtt_device_", "custom_module_set_"]

    def __init__(self, host: str = "localhost", port: str = "29092"):
        self.bootstrap_servers = f"{host}:{port}"
        self.consumer = None
        self.is_running = False
        self.consumer_task = None

    async def start(self) -> None:
        self.consumer = AIOKafkaConsumer(bootstrap_servers=self.bootstrap_servers, metadata_max_age_ms=2 * 60 * 1000)
        await self.consumer.start()

        self.consumer.subscribe(pattern=".*")
        self.is_running = True
        self.consumer_task = asyncio.create_task(self.run_loop())

    async def stop(self) -> None:
        self.is_running = False

        if self.consumer_task:
            self.consumer_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.consumer_task

        if self.consumer:
            await self.consumer.stop()
            self.consumer = None

        server_logger.info("Consumer stopped")

    async def run_loop(self) -> None:
        """Основной цикл чтения сообщений"""
        server_logger.info("Starting consumer loop...")
        if self.is_running:
            try:
                async for message in self.consumer:
                    if not self.is_running:
                        break
                    await self._process_message(message)

            except Exception as e:
                server_logger.error("Error in consumer loop: {}", e)
                raise
            finally:
                await self.stop()

    def _get_device_name(self, topic: str) -> str:
        device_name = ""
        for prefix in self.topic_prefix:
            if prefix in topic:
                device_name = topic.split(prefix)[-1]
                break
        return device_name

    async def _process_message(self, message: ConsumerRecord) -> None:
        message_topic = message.topic
        device_name = self._get_device_name(message_topic)

        if device_name:
            json_message = json.loads(message.value)

            server_logger.info("Receive message in main loop. Topic: {}, message: {}", message_topic, json_message)

            scene_run_task = asyncio.create_task(scene_run(device_name, client_mqtt.client, json_message))
            # add_history_to_cache_task = asyncio.create_task(add_history_to_cache(device_name, json_message))

            background_tasks.add(scene_run_task)
            # background_tasks.add(add_history_to_cache_task)

            scene_run_task.add_done_callback(background_tasks.discard)
            # add_history_to_cache_task.add_done_callback(background_tasks.discard)
