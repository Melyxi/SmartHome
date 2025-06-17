import sys
from pathlib import Path

from loguru import logger

from core.logging import BaseLogger


class LoguruDefaultLoggingConfigurator(BaseLogger):


    def get_console_format(self):
        return "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    def get_format(self):
        return "{time} {level} {message}"

    def check_filter(self, record, logger_type):
        result = record["extra"].get("logger_type") in logger_type
        print(f"Filter check: {result}")  # Должно быть True для scene
        print(f"Filter check: {record}")  # Должно быть True для scene
        return result

    def init_logging(self):
        logger.remove()

        logger.add(
            sys.stdout,
            format=self.get_console_format(),
            filter=lambda r: r["extra"].get("logger_type") in ["server", "scene"],
            colorize=True,
            level=self.log_level
        )

        logger.add(
            str(Path(self.log_dir, "scene.log")),
            rotation="30 days",
            retention="1 year",
            level=self.log_level,
            format=self.get_console_format(),
            filter=lambda r: r["extra"].get("logger_type") == "scene",
            encoding="utf-8"
        )



    @classmethod
    def getLogger(cls, type_logger: str):
        log = logger.bind(logger_type=type_logger)
        return log
