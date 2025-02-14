from backend.configs.config import settings
from backend.core.logging.loguru_configurate_logging import DefaultLoggingConfigurator

default_logging_configurator = settings.get("DEFAULT_LOGGING_CONFIGURATOR", DefaultLoggingConfigurator)
get_logger = default_logging_configurator.getLogger
