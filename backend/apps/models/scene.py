import uuid

from fastapi import UploadFile
from pydantic import BaseModel


class GetScene(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    description: str
    scene: str
    active: bool
    # devices: list[int]

    class Config:
        orm_mode = True


class PostScene(BaseModel):
    name: str
    description: str = ""
    scene: UploadFile
    devices: list[int]
    active: bool = True

class PostSceneWithCode(BaseModel):
    name: str
    description: str = ""
    code: str
    devices: list[int]
    active: bool = True


