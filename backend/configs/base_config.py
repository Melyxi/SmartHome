from pydantic.v1 import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = Field("FastAPI App", env="APP_NAME")
    debug: bool = Field(False, env="DEBUG")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_dotenv_custom_settings()

    def load_dotenv_custom_settings(self):
        pass

    class Config:
        env_file = ".env/.env.base"
        env_file_encoding = "utf-8"
