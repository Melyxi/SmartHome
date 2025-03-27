import uuid

from pydantic import BaseModel


class GetState(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    data: bytes
    time: float

    class Config:
        orm_mode = True


class WebsocketData(BaseModel):
    id: int
    protocol: str
