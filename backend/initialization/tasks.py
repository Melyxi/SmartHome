from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.apps.domain.protocols.task import create_protocols
from backend.apps.domain.states.task import create_states
from backend.core.adapter.tasks import shutdown_event, startup_event

startup_tasks = [startup_event, create_states, create_protocols]
shutdown_tasks = [shutdown_event]


def initialization_tasks(kwargs):
    @asynccontextmanager
    async def lifespan(fastapi_app: FastAPI):
        for task in startup_tasks:
            await task(fastapi_app)
        yield
        for task in shutdown_tasks:
            await task(fastapi_app)

    kwargs.update({"lifespan": lifespan})

    return kwargs
