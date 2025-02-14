from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.extensions import db


async def get_session() -> AsyncSession:
    async with db.async_session() as session:
        yield session
