from fastapi import FastAPI
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.initialization.middleware import initialization_middleware
from backend.core.configurate_logging import get_logger
from backend.initialization import AppInitializer
from backend.initialization.tasks import initialization_tasks
from fastapi.middleware.cors import CORSMiddleware

logger = get_logger("server")


def create_app(
    *_,
    **kwargs,
) -> FastAPI:
    """
        Application factory

    :param _:
    :param kwargs:
    :return:
    """

    from configs.config import settings

    initialization_tasks(kwargs)

    app = FastAPI(**kwargs)

    initialization_middleware(app)

    app_initializer = settings.get("APP_INITIALIZER", AppInitializer)
    app_init = app_initializer(app)
    app_init.init_app()

    logger.info("Initialization app!")
    return app
