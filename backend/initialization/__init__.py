from pathlib import Path

from configs.config import settings
from core.adapter.mqtt_client.client import AsyncClientZigbeeMQTT
from core.configurate_logging import get_logger
# from core.extensions import client_mqtt
from core.logging.loguru_configurate_logging import LoguruDefaultLoggingConfigurator

logger = get_logger("server")


class AppInitializer:
    def __init__(self, app):
        self.app = app

    def init_zigbee_devices(self):
        pass
    #     client_mqtt.mqtt_client.subscribe("zigbee2mqtt/bridge/devices")

    def init_media_root(self):
        media_root = settings.get("MEDIA_ROOT")
        if not media_root:
            logger.warning("Not found MEDIA_ROOT!")
        else:
            media_path = Path(settings.BASE_DIR, media_root)
            media_path.mkdir(parents=True, exist_ok=True)

            upload_scene_dir = settings.get("UPLOAD_SCENE_DIR")
            if not upload_scene_dir:
                logger.warning("Not found UPLOAD_SCENE_DIR!")
            else:
                media_path = Path(settings.BASE_DIR, media_root, upload_scene_dir)
                media_path.mkdir(parents=True, exist_ok=True)

    def init_messages(self) -> None:
        from apps.domain.mqtt.messages import router_message
        AsyncClientZigbeeMQTT.topic_functions.update(router_message)
        # for key, value in router_message.items():
        #     AsyncClientZigbeeMQTT.message_callback_add(key, value)

    def init_routers(self) -> None:
        from apps.routers.button import state_router
        from apps.routers.device import devices_router
        from apps.routers.mqtt import mqtt_router
        from apps.routers.scene import scenes_router


        routers = [devices_router, state_router, mqtt_router, scenes_router]

        for router in routers:
            self.app.include_router(router)

        logger.info("Initialization routers!")

    def pre_init(self):
        pass

    def post_init(self):
        pass

    def init_logging(self) -> None:
        media_path = Path(settings.LOGGING_DIR)
        media_path.mkdir(parents=True, exist_ok=True, mode=0o755)

        default_logging_configurator = settings.get("DEFAULT_LOGGING_CONFIGURATOR", LoguruDefaultLoggingConfigurator)
        default_logging_configurator(settings.get("LOG_LEVEL", "INFO"), settings.LOGGING_DIR).init_logging()
        logger.info("Initialization logging!")

    def init_app(self) -> None:
        self.init_logging()
        self.init_media_root()
        self.pre_init()
        self.init_routers()
        self.init_messages()
        self.init_zigbee_devices()
        self.post_init()
