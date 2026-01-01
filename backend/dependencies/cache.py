from core.cache.base.backend import BaseCache
from fastapi import Request


async def get_cache(request: Request) -> BaseCache:
    return request.app.state.cache
