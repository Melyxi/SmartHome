from extensions import db
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    async with db.async_session() as session:
        yield session
