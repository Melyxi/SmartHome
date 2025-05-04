import asyncio
from contextlib import asynccontextmanager

from apps.domain.devices.task import sync_create_devices
from apps.domain.mqtt.task import shutdown_mqtt
from core.adapter.tasks import shutdown_event, startup_event
from fastapi import FastAPI

startup_tasks = [sync_create_devices, startup_event]
shutdown_tasks = [shutdown_event, shutdown_mqtt]


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
