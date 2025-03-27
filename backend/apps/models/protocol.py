import uuid
from datetime import datetime

from pydantic import BaseModel


class GetProtocol(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    description: str
    type: str

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostProtocol(BaseModel):
    name: str
    description: str
    type: str

    class Config:
        orm_mode = True
