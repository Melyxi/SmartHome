import uuid
from datetime import datetime

from apps.models.button import GetButton
from apps.models.protocol import GetProtocol
from pydantic import BaseModel


class GetShortDevice(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    unique_name: str
    description: str

class GetDevice(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    unique_name: str
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
    unique_name: str
    description: str | None = ""
    css: str | None = ""
    html: str | None = ""

    protocol_id: int
    buttons: list[int]


class PutDevice(BaseModel):
    name: str
    unique_name: str
    description: str | None = ""
    css: str | None = ""
    html: str | None = ""

    protocol_id: int
    buttons: list[int]