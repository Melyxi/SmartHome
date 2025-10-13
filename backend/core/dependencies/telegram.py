from aiogram import Bot, Dispatcher
from core.backends.telegram import bot, dp


async def get_bot() -> Bot:
    return bot

async def get_dispatcher() -> Dispatcher:
    return dp
