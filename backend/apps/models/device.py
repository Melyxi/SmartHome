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
    built_html: str

    protocol: GetProtocol

    buttons: list[GetButton]

    created_at: datetime
    updated_at: datetime
    exposes: list

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


class PatchDevice(BaseModel):
    name: str | None = None
    unique_name: str | None = None
    description: str | None = ""
    css: str | None = ""
    html: str | None = ""

    protocol_id: int | None = None
    buttons: list[int] | None = None

    class Config:
        extra = "forbid"