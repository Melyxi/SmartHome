import contextlib

import aiogram
from core.extensions import telegram_bot


class TelegramNotification:

    @classmethod
    async def send(cls, message: str, username: str | None = None):
        if telegram_bot:
            with contextlib.suppress(aiogram.exceptions.TelegramUnauthorizedError):
                chat_ids = [] # TODO Add chat id's user
                for _id in chat_ids:
                    await telegram_bot.send_message(chat_id=_id, text=message)

    async def info(self):
        pass

