from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import config as cfg
from src.database.db import Database
import logging

html= types.ParseMode.HTML#<- &lt; >- &gt; &- &amp; 
mark= types.ParseMode.MARKDOWN
v2= types.ParseMode.MARKDOWN_V2


bot = Bot(token= cfg.TOKEN)
logging.basicConfig(level=logging.INFO)
dp= Dispatcher(bot=bot, storage=MemoryStorage())
db = Database('src/database/database.db')

class Focus(StatesGroup):
    action= State()
    category= State()
    log= State()
    enter= State()
    Q5= State()
    
class Friend(StatesGroup):
    name= State()