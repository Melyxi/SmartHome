from pydantic.v1 import BaseModel


class DBAccount(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
