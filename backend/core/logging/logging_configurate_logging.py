import logging
import sys
from pathlib import Path

from core.logging import BaseLogger

class LoggingDefaultLoggingConfigurator(BaseLogger):

    def get_format(self):
        return "{time} {level} {message}"

    def configurate_logging_config(self) -> dict:
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": self.log_level,
                    "formatter": "default",
                    "stream": sys.stdout,
                },
                "file_scene": {
                    "level": self.log_level,
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filters": [],
                    "filename": str(Path(self.log_dir, "scene.log")),
                    "formatter": "default",
                    "when": "D",
                    "interval": 30,
                    "backupCount": 12,
                }

            },
            "loggers": {
                "server": {
                    "level": self.log_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
                "scene": {
                    "level": self.log_level,
                    "handlers": ["console", "file_scene"],
                    "propagate": False,
                },

            },
        }
        return LOGGING_CONFIG


    def init_logging(self):
        logging.config.dictConfig(self.configurate_logging_config())

    @classmethod
    def getLogger(cls, type_logger):
        log = logging.getLogger(type_logger)
        return log
