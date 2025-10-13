from core.extensions import cache


async def cache_startup_event(app):
    app.state.cache = cache

async def cache_shutdown_event(app):
    await app.state.cache.close()
