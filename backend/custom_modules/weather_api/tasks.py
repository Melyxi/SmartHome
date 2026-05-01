import asyncio
import contextlib

from fastapi import FastAPI
from weather_api.main import MainWeatherManager


async def startup_event(app: FastAPI) -> None:
    try:
        main_manager = MainWeatherManager(app)
        app.state.weather_api = asyncio.create_task(main_manager.background_worker())
    except Exception:
       print("Something went wrong") 

async def shutdown_event(app: FastAPI) -> None:
    if hasattr(app.state, "weather_api"):
        app.state.weather_api.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await app.state.weather_api
