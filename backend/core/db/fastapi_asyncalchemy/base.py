from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from backend.configs.config import settings
from backend.core.db.utils import make_url_safe

from backend.core.configurate_logging import get_logger

logger = get_logger("server")

def sqlalchemy_engine_options() -> dict:
    # This block sets the default isolation level for mysql to READ COMMITTED if not
    # specified in the config. You can set your isolation in the config by using
    # SQLALCHEMY_ENGINE_OPTIONS
    eng_options = settings.get("SQLALCHEMY_ENGINE_OPTIONS", {})
    isolation_level = eng_options.get("isolation_level")
    set_isolation_level_to = None
    if not isolation_level:
        backend = make_url_safe(settings.get("DATABASE_URL")).get_backend_name()
        if backend in ("mysql", "postgresql"):
            set_isolation_level_to = "READ COMMITTED"

    if set_isolation_level_to:
        logger.info(
            "Установка для БД уровня изоляции %s",
            set_isolation_level_to,
        )
        eng_options["isolation_level"] = set_isolation_level_to
    return eng_options


class SQLA:
    Base = declarative_base()
    engine = create_async_engine(settings.get("DATABASE_URL"), echo=True, execution_options=sqlalchemy_engine_options())


    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


    engine = create_engine(settings.get("DATABASE_URL").replace("asyncpg", "psycopg2"), echo=True)


    sync_session = sessionmaker(
                        bind=engine,
                        autocommit=False,
                        autoflush=False,
                        expire_on_commit=False
        )
    @classmethod
    async def get_session(cls) -> AsyncSession:
        async with cls.async_session() as session:
            yield session
