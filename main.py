from email.message import Message
from db import Databae
import config as cfg
import keyboard as nav
from datetime import datetime, timedelta, date
import calendar

import logging
from aiogram import Bot, executor, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

bot = Bot(token=cfg.TOKEN)
logging.basicConfig(level=logging.INFO)
dp= Dispatcher(bot=bot, storage=MemoryStorage())
db= Databae('database.db')

html= types.ParseMode.HTML
mark= types.ParseMode.MARKDOWN
v2= types.ParseMode.MARKDOWN_V2

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message, state: FSMContext):
    await message.answer(f"Hello! This is a bot for tracking your daily activities. What is your goal?", reply_markup=nav.main_menu)
    
    
if __name__ == '__main__':
    executor.start_polling(dp)