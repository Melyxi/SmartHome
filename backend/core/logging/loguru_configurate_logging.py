import sys

from loguru import logger


class DefaultLoggingConfigurator:
    def __init__(self):
        self.format = ""

    def get_format(self):
        return "{time} {level} {message}"

    def init_logging(self):
        logger.add(
            sys.stdout,
            filter=lambda record: record["extra"].get("log_type") == "server",
            format="{time} {level} {message}",
        )

    @classmethod
    def getLogger(cls, type_logger):
        log = logger.bind(log_type=type_logger)
        return log
