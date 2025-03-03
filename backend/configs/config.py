import os
from functools import lru_cache
from typing import Any

from backend.configs.base_config import Settings
from backend.configs.dev_config import DevSettings
from backend.configs.prod_config import ProdSettings


DEBUG = True if os.environ.get("DEBUG", False) == "True" else False
if DEBUG:
    load_settings = DevSettings
else:
    load_settings = ProdSettings


@lru_cache()
def get_settings() -> Settings:
    return load_settings()


class LazySettings:
    def __getattr__(self, item: str) -> Any:
        return getattr(get_settings(), item)

    def get(self, item: str, default: Any = None) -> Any:
        try:
            return getattr(self, item)
        except AttributeError:
            return default


settings = LazySettings()
