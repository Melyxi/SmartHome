from core.cache.mongodb.backend import MongoDBSCache
from core.db.fastapi_asyncalchemy.base import SQLA

db = SQLA()

cache = MongoDBSCache("mongodb://localhost:27017", "test_db")
