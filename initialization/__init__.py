from contextlib import asynccontextmanager
from functools import partial
import asyncio

from core.adapter.tasks import startup_event, shutdown_event
from core.configurate_logging import DefaultLoggingConfigurator
from configs.config import settings
from core.configurate_logging import get_logger


logger = get_logger("server")

startup_tasks = [startup_event]
shutdown_tasks = [shutdown_event]


class AppInitializer:
    def __init__(self, app):
        self.app = app

    def init_routers(self) -> None:
        from api import router

        routers = [router]

        for router in routers:
            self.app.include_router(router)

        logger.info("Initialization routers!")

    def pre_init(self):
        pass

    def post_init(self):
        pass

    def init_logging(self) -> None:
        default_logging_configurator = settings.get("DEFAULT_LOGGING_CONFIGURATOR", DefaultLoggingConfigurator)
        default_logging_configurator().init_logging()
        logger.info("Initialization logging!")


    def init_app(self) -> None:
        self.init_logging()
        self.pre_init()
        self.init_routers()
        self.post_init()
