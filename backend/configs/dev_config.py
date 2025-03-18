import os

from pydantic.v1 import Field

from backend.configs.base_config import Settings
from backend.core.logging.logging_configurate_logging import LoggingDefaultLoggingConfigurator


class DevSettings(Settings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    TRANSMITTER_HOST: str = Field(..., env="TRANSMITTER_HOST")
    TRANSMITTER_PORT: int = Field(..., env="TRANSMITTER_PORT")

    DEFAULT_LOGGING_CONFIGURATOR = LoggingDefaultLoggingConfigurator
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = ".env/.env.dev"
        env_file_encoding = "utf-8"
