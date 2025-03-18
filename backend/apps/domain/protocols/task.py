import contextlib

from sqlalchemy.exc import IntegrityError

from apps.repositories.protocol import ProtocolSqlAlchemyRepository
from core.enums import ProtocolType
from core.extensions import db

protocols = [
    {
        "uuid": "d85b7f3a-f66b-42aa-964a-f368f62ba5df",
        "name": "Radio wave 433MHz",
        "description": "Radio wave 433MHz",
        "type": ProtocolType.RADIO_433MHz.value,
    }
]


async def create_protocols(*args):
    async with db.async_session() as session:
        repository = ProtocolSqlAlchemyRepository(session)
        for protocol in protocols:
            with contextlib.suppress(IntegrityError):
                await repository.create(**protocol)
