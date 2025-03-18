import uuid
from datetime import datetime

from pydantic.v1 import BaseModel


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