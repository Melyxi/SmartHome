import uuid

from apps.models.device import ShortGetDevice
from fastapi import UploadFile
from pydantic import BaseModel


class GetScene(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    description: str
    scene: str
    active: bool

    class Config:
        orm_mode = True

class GetSceneWithDevices(GetScene):
    devices: list[ShortGetDevice]


class GetSceneWithCode(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    description: str
    scene: str
    active: bool
    code: str

    class Config:
        orm_mode = True

class GetSceneWithCodeWithDevices(GetSceneWithCode):
    devices: list[ShortGetDevice]


class PostScene(BaseModel):
    name: str
    description: str = ""
    scene: UploadFile
    devices: list[int]
    active: bool = True


class PatchScene(BaseModel):
    name: str | None = None
    description: str = ""
    scene: UploadFile | None = None
    devices: list[int] | None = None
    active: bool | None = None

class PatchSceneWithCode(BaseModel):
    name: str | None = None
    description: str = ""
    code: str | None = None
    devices: list[int] | None = None
    active: bool = True

class PostSceneWithCode(BaseModel):
    name: str
    description: str = ""
    code: str
    devices: list[int]
    active: bool = True


