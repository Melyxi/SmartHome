from configs.config import settings
from core.configurate_logging import get_logger
from core.logging.loguru_configurate_logging import DefaultLoggingConfigurator

logger = get_logger("server")


class AppInitializer:
    def __init__(self, app):
        self.app = app

    def init_routers(self) -> None:
        from apps.routers.button import state_router
        from apps.routers.device import devices_router
        from apps.routers.mqtt import mqtt_router

        routers = [devices_router, state_router, mqtt_router]

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
