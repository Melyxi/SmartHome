import logging
import sys

# Словарь с конфигурацией логгера
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": sys.stdout,
        }
    },
    "loggers": {
        "server": {
            "level": "DEBUG",  # Здесь используется self.DEFAULT_LOGGING_LEVEL
            "handlers": ["console"],
            "propagate": False,
        }
    },
}


class LoggingDefaultLoggingConfigurator:
    def __init__(self):
        self.format = ""

    def get_format(self):
        return "{time} {level} {message}"

    def init_logging(self):
        logging.config.dictConfig(LOGGING_CONFIG)

    @classmethod
    def getLogger(cls, type_logger):
        log = logging.getLogger(type_logger)
        return log
