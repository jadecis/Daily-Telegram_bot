from cgitb import text
from email.message import Message
from db import Databae
import config as cfg
import keyboard as nav
from datetime import datetime, timedelta, date
import calendar
import asyncio
import aioschedule

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
    
@dp.callback_query_handler(text= 'start')
async def answer_message(call: types.CallbackQuery):
    await call.message.answer(
        f"Great! This bot helps you to record how much time you spent on various activities. The bot will store and show you how productive you were in different days, weeks and months.\n\nNow let's record your first activity!", reply_markup=nav.record_button) 

@dp.message_handler(commands=['stat'])
async def start_message(message: types.Message, state: FSMContext):
    await message.answer(f"Test", reply_markup=nav.stat_menu(day='today', split='by actions'))
                         
@dp.callback_query_handler(text_contains= 'stat_')
async def answer_message(call: types.CallbackQuery):
    print(call.data)
    if call.data == 'stat_all':
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=nav.choose_action_menu(list_actions=[]))
    elif call.data == 'stat_today_by actions' or call.data == 'stat_today_by records':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='week', split='by actions'))
    elif call.data == 'stat_week_by actions' or call.data == 'stat_week_by day':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='month', split='by actions'))
    elif call.data == 'stat_month_by actions'or call.data == 'stat_month_by week':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='all', split='by actions'))
    elif call.data == 'stat_all_by actions' or call.data == 'stat_all_by week':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='today', split='by actions'))
    
    elif call.data == 'stat_today_by actions_':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='today', split='by records'))
    elif call.data == 'stat_today_by records_':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='today', split='by actions'))
    
    elif call.data == 'stat_week_by actions_':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='week', split='by day'))
    elif call.data == 'stat_week_by day_':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='week', split='by actions'))
        
    elif call.data == 'stat_month_by actions_':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='month', split='by week'))
    elif call.data == 'stat_month_by week_':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='month', split='by actions'))   
    
    elif call.data == 'stat_all_by actions_':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='all', split='by week'))
    elif call.data == 'stat_all_by week_':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='all', split='by actions'))

@dp.callback_query_handler(text_contains= 'choose_')
async def answer_message(call: types.CallbackQuery, state: FSMContext):
    data= await state.get_data()
    actions_list= []
    if data.get('actions') != None:
        for act in data.get('actions'):
            actions_list.append(act)
    if call.data == 'choose_done':
        await call.message.edit_text(f"Test", reply_markup=nav.stat_menu(day='today', split='by actions'))
        print(data.get('actions'))
    elif call.data == 'choose_reset':
        actions_list.clear()
        await state.update_data(actions=actions_list)
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=nav.choose_action_menu(list_actions=[]))
    else:
        action= call.data.split('_')[1]
        actions_list.append(action)
        await state.update_data(actions=actions_list)
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=nav.choose_action_menu(list_actions=actions_list))
              
#Notification
async def every_mon():
    await dp.bot.send_message(chat_id=849253641, text=f"🎉 It was a great week!\nYou got ⭐️140 for this 7 days")
    
async def scheduler():
    aioschedule.every().monday.at("10:00").do(every_mon)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def notification(_):
    asyncio.create_task(scheduler())




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=notification)