from loader import dp
from aiogram.utils import executor
from aiogram.types import BotCommand
from src.commands import command
from src.handlers import start 
from src.handlers import friend
from src.handlers import focus
from src.handlers import stat
from src.notify.notifi import scheduler
import asyncio



async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand("start", "restart bot"),
        BotCommand("stat", "Your stats"),
        BotCommand("focus", "Log activity"),
        BotCommand("friends", "Your friends")
    ])

async def start(dp):
    await set_default_commands(dp)
    asyncio.create_task(scheduler())

executor.start_polling(dp, skip_updates=False ,on_startup=start)