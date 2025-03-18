import uuid
from datetime import datetime

from pydantic.v1 import BaseModel

from apps.models.button import GetButton
from apps.models.protocol import GetProtocol


class GetDevice(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    description: str
    css: str
    html: str

    protocol: GetProtocol

    buttons: list[GetButton]

    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True