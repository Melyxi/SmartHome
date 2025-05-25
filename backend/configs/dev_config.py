import os

from configs.base_config import Settings
from core.logging.logging_configurate_logging import LoggingDefaultLoggingConfigurator
from pydantic.v1 import Field


class DevSettings(Settings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    TRANSMITTER_HOST: str = Field(..., env="TRANSMITTER_HOST")
    TRANSMITTER_PORT: int = Field(..., env="TRANSMITTER_PORT")

    MQTT_HOST: str = Field(..., env="MQTT_HOST")
    MQTT_PORT: int = Field(..., env="MQTT_PORT")

    DEFAULT_LOGGING_CONFIGURATOR = LoggingDefaultLoggingConfigurator
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = ".env/.env.dev"
        env_file_encoding = "utf-8"
