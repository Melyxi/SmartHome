from typing import Any

from core.cache.base.backend import BaseCache
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBSCache(BaseCache):
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def get(self, key: str) -> dict[str, Any] | None:
        return await self.db.items.find_one({"_id": key})

    async def set(self, key: str, value: dict[str, Any]) -> None:
        await self.db.items.update_one(
            {"_id": key}, {"$set": value}, upsert=True
        )

    async def delete(self, key: str) -> bool:
        result = await self.db.items.delete_one({"_id": key})
        return result.deleted_count > 0

    async def close(self) -> None:
        self.client.close()
