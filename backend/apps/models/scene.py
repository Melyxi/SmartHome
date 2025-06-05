import uuid

from pydantic import BaseModel


class GetScene(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    description: str
    scene: str
    # devices: list[int]

    class Config:
        orm_mode = True
