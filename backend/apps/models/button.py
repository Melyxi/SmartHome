import uuid
from datetime import datetime

from pydantic import BaseModel

from apps.models.state import GetState


class GetMetaButton(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    css: str
    html: str
    type: str

    class Config:
        orm_mode = True


class GetButton(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    description: str
    meta_button: GetMetaButton
    states: list[GetState]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostButton(BaseModel):
    name: str
    description: str
    meta_button_id: int
    states: list[GetState]
