import contextlib

from sqlalchemy.exc import IntegrityError

from apps.repositories.protocol import ProtocolSqlAlchemyRepository
from core.enums import ProtocolType, ButtonType
from core.extensions import db

meta_buttons = [
    {
        "uuid": "6767f186-d729-4bfa-8e03-eaa76ef9a418",
        "name": "Кнопка А",
        "css": "",
        "html": "",
        "type": ButtonType.BUTTON.value,
    }
]

buttons = [
    {
        "uuid": "d008cd32-48af-4382-8c48-ac4f57e1d155",
        "name": "Включить реле",
        "description": "",

    }
]


async def create_buttons(*args):
    pass