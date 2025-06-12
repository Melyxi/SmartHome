import os

from pydantic.v1 import Field

from configs.base_config import Settings
from core.logging.logging_configurate_logging import LoggingDefaultLoggingConfigurator


class DevSettings(Settings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    TRANSMITTER_HOST: str = Field(..., env="TRANSMITTER_HOST")
    TRANSMITTER_PORT: int = Field(..., env="TRANSMITTER_PORT")

    MQTT_HOST: str = Field(..., env="MQTT_HOST")
    MQTT_PORT: int = Field(..., env="MQTT_PORT")

    CACHE_URL: str = Field(..., env="CACHE_URL")
    CACHE_TABLE: str = Field(..., env="CACHE_TABLE")

    DEFAULT_LOGGING_CONFIGURATOR = LoggingDefaultLoggingConfigurator
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    MEDIA_ROOT = "media/"

    class Config:
        env_file = ".env/.env.dev"
        env_file_encoding = "utf-8"
