import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from configs.config import settings


def create_bot() -> Bot | None:
    if settings.TELEGRAM_BOT_TOKEN:
        return Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def create_dispatcher() -> Dispatcher:
    return Dispatcher()


bot = create_bot()
dp = create_dispatcher()


background_tasks = set()


async def run_polling_non_blocking():
    if settings.TELEGRAM_BOT_TOKEN:
        try:
            await dp.start_polling(bot, handle_signals=False)
        except asyncio.CancelledError:
            print("Polling was cancelled")
            raise
        except Exception as e:
            print(f"Polling failed: {e}")
            raise


async def telegram_bot_startup_event(app):
    if settings.TELEGRAM_BOT_TOKEN:
        task = asyncio.create_task(run_polling_non_blocking())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)


async def telegram_bot_shutdown_event(app):
    if settings.TELEGRAM_BOT_TOKEN:
        await dp.stop_polling()
        await bot.session.close()
        for task in background_tasks:
            task.cancel()
        await asyncio.gather(*background_tasks, return_exceptions=True)



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {message.chat.username} your id is {message.chat.id}!")