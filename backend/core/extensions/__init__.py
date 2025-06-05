from configs.config import settings
from core.cache.mongodb.backend import MongoDBSCache
from core.db.fastapi_asyncalchemy.base import SQLA

db = SQLA()

cache = MongoDBSCache(settings.get("CACHE_URL"), settings.get("CACHE_TABLE"))
