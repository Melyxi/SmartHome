import uuid
from datetime import datetime

from pydantic import BaseModel, Field

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
        from_attributes = True


class PostDevice(BaseModel):
    name: str
    description: str | None = ""
    css: str | None = ""
    html: str | None = ""

    protocol_id: int
    buttons: list[int]
