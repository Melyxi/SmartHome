from core.extensions import cache


async def startup_cache(app):
    app.state.cache = cache

async def shutdown_cache(app):
    await app.state.cache.close()