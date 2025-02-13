from pydantic.v1 import Field

from configs.base_config import Settings
from core.logging.logging_configurate_logging import LoggingDefaultLoggingConfigurator
from core.logging.loguru_configurate_logging import DefaultLoggingConfigurator


class DevSettings(Settings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    TRANSMITTER_HOST: str = Field(..., env="TRANSMITTER_HOST")
    TRANSMITTER_PORT: int = Field(..., env="TRANSMITTER_PORT")


    DEFAULT_LOGGING_CONFIGURATOR = LoggingDefaultLoggingConfigurator

    class Config:
        env_file = ".env/.env.dev"
        env_file_encoding = "utf-8"
