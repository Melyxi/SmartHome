from apps.repositories.state import StateSqlAlchemyRepository
from core.extensions import db


states = [{"uuid": "d85b7f3a-f66b-42aa-964a-f368f62ba5df"}]


async def create_states(app):
    async with db.async_session() as session:
        repository = StateSqlAlchemyRepository(session)

    print("Init States")
