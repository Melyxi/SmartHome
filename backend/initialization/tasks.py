import asyncio
from contextlib import asynccontextmanager

from adapters.broker.tasks import shutdown_broker_consumer, startup_broker_consumer
from apps.domain.devices.task import sync_create_devices
from apps.domain.mqtt.task import shutdown_mqtt, startup_mqtt
from core.adapter.tasks import shutdown_event, startup_event
from core.configurate_logging import get_logger
from core.tasks.broker import shutdown_broker_producer, startup_broker_producer
from fastapi import FastAPI
from initialization.cache.tasks import shutdown_cache, startup_cache
from initialization.modules_registration import ModuleRegistry

server_logger = get_logger("server")


modules_startup_events, modules_shutdown_events = ModuleRegistry.get_tasks()


startup_tasks = [
    startup_broker_producer,
    startup_mqtt,
    sync_create_devices,
    startup_event,
    startup_cache,
    startup_broker_consumer,
] + modules_startup_events
shutdown_tasks = [
    shutdown_broker_producer,
    shutdown_mqtt,
    shutdown_event,
    shutdown_cache,
    shutdown_broker_consumer,
] + modules_shutdown_events


def initialization_tasks(kwargs):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        for task in startup_tasks:
            if asyncio.iscoroutinefunction(task):
                await task(app)
            else:
                await asyncio.to_thread(task, app)

        yield

        for task in shutdown_tasks:
            if asyncio.iscoroutinefunction(task):
                await task(app)
            else:
                await asyncio.to_thread(task, app)

    kwargs.update({"lifespan": lifespan})
    return kwargs
