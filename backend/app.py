from core.configurate_logging import get_logger
from fastapi import FastAPI
from initialization import AppInitializer
from initialization.middleware import initialization_middleware
from initialization.tasks import initialization_tasks

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
