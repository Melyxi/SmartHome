from pydantic.v1 import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = Field("FastAPI App", env="APP_NAME")
    debug: bool = Field(False, env="DEBUG")

    class Config:
        env_file = ".env/.env.base"
        env_file_encoding = "utf-8"