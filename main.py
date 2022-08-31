from email import message
from os import stat
from urllib.parse import ParseResultBytes
from db import Databae
import config as cfg
import keyboard as nav
from datetime import datetime, time, timedelta, date
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

class Focus(StatesGroup):
    Q1= State()
    Q2= State()
    Q3= State()
    Q4= State()
    
html= types.ParseMode.HTML#<- &lt; >- &gt; &- &amp; 
mark= types.ParseMode.MARKDOWN
v2= types.ParseMode.MARKDOWN_V2

def get_stat_by_action(stat_list, actions_list, week=False):
    points = {}
    hours = {}
    decimal= 1 if week is False else 0.1
    categories=True
    message=""
    total_hours= 0.0
    total_points= 0.0
    if len(actions_list) != 0:  
        for stat in stat_list:
            if list(actions_list).__contains__(stat[0]):
                if stat[0] in points:
                    points[stat[0]]+= stat[2]
                    hours[stat[0]]+= stat[1]
                else:
                    points[stat[0]]= stat[2]
                    hours[stat[0]]= stat[1]
    else:
        for stat in stat_list:
            if stat[0] in points:
                points[stat[0]]+= stat[2]
                hours[stat[0]]+= stat[1]
            else:
                points[stat[0]]= stat[2]
                hours[stat[0]]= stat[1]
    if categories is True:
        if len(hours) != 0:
            for name in hours:
                total_hours+=hours[name]
                total_points += points[name]
                hours_name= f'&lt;{decimal}' if hours[name] > 0 and hours[name] < decimal else hours[name] 
                if type(hours_name) != str: hours_name= int(hours_name) if week is False else round(hours_name, 1)
                message+= f"\n{name} 🕝{hours_name}/ ⭐️{int(points[name])}"
            hours_name_total= f'&lt;{decimal}' if (total_hours > 0) and (total_hours < decimal) else total_hours
            if type(hours_name_total) == float: hours_name_total= int(total_hours) if week is False else round(hours_name_total, 1)
            message+= f"\n\n<b>Total</b>: 🕝{hours_name_total}/ ⭐️{int(total_points)}"
            return message
        else: return "\nYou haven't been active or you haven't been active this action during this interval of time"
    else:
        if len(hours) != 0:
            for name in hours:
                total_hours+=hours[name]
                hours_name= f'&lt;{decimal}' if hours[name] > 0 and hours[name] < decimal else hours[name]
                if type(hours_name) != str: hours_name= int(hours_name) if week is False else round(hours_name, 1)
                message+= f"\n{name} 🕝{hours_name}"
            hours_name_total= f'&lt;{decimal}' if (total_hours > 0) and (total_hours < decimal) else total_hours
            if type(hours_name_total) == float: hours_name_total= int(hours_name_total) if week is False else round(hours_name_total, 1)
            message+= f"\n\n<b>Total</b>: 🕝{hours_name_total}"
            return message
        else: return "\nYou haven't been active or you haven't been active this action during this interval of time"
    
def get_stat_by_week(user_id, actions_list, first_date, second_date):
    message= ""
    categories= True
    while first_date <= second_date:
        total_hours= 0.0
        total_points= 0.0
        result= db.stat_by_interval(user_id=user_id, first_date=first_date, second_date=first_date+ timedelta(weeks=1))
        if len(actions_list) != 0:
            for stat in result:
                if list(actions_list).__contains__(stat[0]):
                    total_hours+=stat[1]
                    total_points+= stat[2]
        else:
            for stat in result:
                total_hours+=stat[1]
                total_points+= stat[2]
        if categories is True:
            hours= '&lt;1' if (total_hours > 0) and (total_hours < 1) else int(total_hours)
            message+=f"\n{first_date.strftime('%d-%b')} 🕝{hours}/ ⭐️{int(total_points)}"
        else:
            hours= '&lt;1' if total_hours > 0 and total_hours < 1 else int(total_hours)
            message+=f"\n{first_date.strftime('%d-%b')} 🕝{hours}"
        first_date += timedelta(weeks=1)       
    return message
            
def get_stat_by_records(stat_list, actions_list):
    message=""
    categories= True
    if len(actions_list) != 0:  
        for stat in stat_list:
            if list(actions_list).__contains__(stat[0]):
                duration= f'({stat[4]})' if stat[4] != None else ""
                hour= '&lt;0.1' if stat[1] > 0 and stat[1] < 0.1 else round(stat[1], 1)
                if categories is True:
                    message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} / ⭐️{int(stat[2])} {duration}"
                else:
                    message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} {duration}"
        if message == "":
            return "\nYou haven't been active this action during this interval of time"
        else:
            return message
    else:
        if len(stat_list) == 0:
            return "\nYou haven't been active during this interval of time"
        else:
            for stat in stat_list:
                duration= f'({stat[4]})' if stat[4] != None else ""
                hour= '&lt;0.1' if stat[1] > 0 and stat[1] < 0.1 else round(stat[1], 1)
                if categories is True:
                    message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} / ⭐️{int(stat[2])} {duration}"
                else:
                    message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} {duration}"
            return message
        
def get_stat_by_day(user_id, action_list, first_date, second_date):
    message= ""
    categories= True
    while first_date < second_date:
        result= db.stat_today(user_id=user_id, date=first_date)
        print(result)
        total_hours = 0.0
        total_points = 0.0
        for stat in result:
            if len(action_list) != 0:
                if list(action_list).__contains__(stat[0]):
                    total_hours+= stat[1]
                    total_points+=stat[2]
            else:
                total_hours+= stat[1]
                total_points+=stat[2]
        hours= '&lt;0.1' if total_hours > 0 and total_hours < 0.1 else round(total_hours, 1)
        if categories is True:
            message+= f"\n{first_date.strftime('%a')} 🕝{hours} / ⭐️{int(total_points)}"
        else:
            message+= f"\n{first_date.strftime('%a')} 🕝{hours}"
        first_date += timedelta(1)
    return message

@dp.message_handler(commands=['start'], state=Focus.all_states)
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message, state: FSMContext):
    await state.finish()
    if db.user_info(user_id=message.chat.id) == None:
        db.add_user(user_id=message.chat.id)
    await message.answer(f"Hello! This is a bot for tracking your daily activities. What is your goal?", reply_markup=nav.main_menu)

@dp.callback_query_handler(text= 'start')
async def answer_message(call: types.CallbackQuery):
    await call.message.answer(
    f"Great! This bot helps you to record how much time you spent on various activities. The bot will store and show you how productive you were in different days, weeks and months.\n\nNow let's record your first activity!", reply_markup=nav.record_button) 
    
@dp.message_handler(commands=['friends'], state=Focus.all_states)
@dp.message_handler(commands=['friends'])
async def friends_message(message: types.Message, state: FSMContext):
    if db.user_info(user_id=message.chat.id)[3] == None:
        await message.answer(f"You don't have any friends yet. Add them!", reply_markup=nav.add_friends_button)
    else: 
        pass
    
    
@dp.message_handler(commands=['focus'], state=Focus.all_states)
@dp.message_handler(commands=['focus'])
async def start_message(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        float(message.text[7:])
        await state.update_data(date=message.text[7:])
    except  Exception as ex:
        print(ex)
    
    messages= ""
    if len(db.inf_about_action(user_id=message.chat.id)) == 0:
        messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
    else:
        messages="Select or type <b>activity</b>🏄‍♂️"
    
    await message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=message.chat.id), parse_mode=html)
    await Focus.Q1.set()

@dp.callback_query_handler(text_contains= 'record')
async def record_answer(call: types.CallbackQuery, state: FSMContext):
    messages= ""
    
    if len(db.inf_about_action(user_id=call.message.chat.id)) == 0:
        messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
    else:
        messages="Select or type <b>activity</b>🏄‍♂️"
    
    await call.message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=call.message.chat.id), parse_mode=html)
    await Focus.Q1.set()

@dp.message_handler(content_types=['text'], state=Focus.Q1)
async def q1_answer(message: types.Message, state: FSMContext):
    act= message.text
    res=db.inf_about_action(user_id=message.chat.id)
    for act_res in res:
        act_res[0].lower()
        if act_res[0].lower()== act.lower():
            await message.answer(f"You already have this 🏄‍♂️{act}\nType new <b>activity</b>", parse_mode=html)
            await Focus.Q1.set()
            return
    await message.answer(f"🏄‍♂️{act}\nSelect the level of 🚦<b>usefulness</b> of activity", reply_markup=nav.categories_menu(), parse_mode=html)
    await state.update_data(action_name=act)
    db.add_action(user_id=message.chat.id, action= act)
    await Focus.Q2.set()
    
@dp.callback_query_handler(text_contains= 'act_', state=Focus.Q1)
async def act_answer(call: types.CallbackQuery, state: FSMContext):
    act= call.data.split('_')[1]
    skip_inf= int(db.user_info(user_id=call.message.chat.id)[2])
    if skip_inf > 4:
        await call.message.edit_text(f"🏄‍♂️ {act}\n\nStart recording or have you already performed the action?", reply_markup=nav.log_menu, parse_mode=html)
    else:
        await call.message.edit_text(f"🏄‍♂️{act}\n\nSelect the level of 🚦<b>usefulness</b> of activity", reply_markup=nav.categories_menu(), parse_mode=html)
        await state.update_data(action_name=act)
        await Focus.Q2.set()
           
@dp.callback_query_handler(text_contains= 'cat_', state=Focus.Q2)
async def cat_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cat= call.data.replace('cat_', '')
    act= data.get('action_name')
    if cat== 'Skip':
        db.skip_user(call.message.chat.id)
        await call.message.edit_text(f"🏄‍♂️ {act}\n\nStart recording or have you already performed the action?", reply_markup=nav.log_menu, parse_mode=html)
    else:
        point_= call.data.split('_')[2]
        await state.update_data(point=point_)
        await state.update_data(category=cat)
        db.skip_user(call.message.chat.id, sk=False)
        await call.message.edit_text(f"🏄‍♂️ {act} /🚦{cat.split('_')[0]} useful\n\nStart recording or have you already performed the action?", reply_markup=nav.log_menu, parse_mode=html)
    await Focus.Q2.set()

@dp.callback_query_handler(text_contains= 'log_', state=Focus.Q2)
async def log_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    act= data.get('action_name') 
    cat= f" /🚦 {data.get('category').split('_')[0]} useful" if data.get('category') != None else ""
    if call.data == 'log_enter':
        await call.message.edit_text(f"🏄‍♂️ {act}{cat}\n\nEnter duration🕝 (example: 1,5 or 1:30)", parse_mode=html)
        await Focus.Q3.set()
    if call.data == "start":
        pass

@dp.message_handler(content_types=['text'], state=Focus.Q3)
async def q1_answer(message: types.Message, state: FSMContext):
    try:
        if message.text.__contains__(':'):
            float(message.text.replace(':', '.'))
            time= message.text.split(':')
            hours= (int(time[0].strip()) + float(time[1].strip()) / 60)
        elif message.text.__contains__(','):
            hours= float(message.text.replace(',', '.'))
        else:
           hours= float(message.text)
        data = await state.get_data()
        date_log= date.today() if data.get('date') == None else date(year=date.today().year, month=int(data.get('date').split('.')[1]), day= int(data.get('date').split('.')[0]))
        await state.update_data(date=date_log)
        category = '' if data.get('category') == None else data.get('category').split('_')[0]
        act= data.get('action_name')
        point= int(data.get('category').split('_')[1]) * hours
        await state.update_data(points=point)
        db.add_focus(user_id=message.chat.id, action=act, hour=hours, date=date_log, category=category, point=point)
        view_date= "" if data.get('date') == None else date_log.strftime('%a, %d.%m')
        category= f" /🚦{category} useful"
        hours= '&lt;0.1' if hours < 0.1 and hours > 0 else round(hours, 1)
        await state.update_data(hour=hours)
        if date_log == date.today():
            await message.answer(f"{view_date}\n🎉 Added 🕝{hours} / ⭐️{int(point)}\n 🏄‍♂️{act}{category}", reply_markup=nav.focus_menu, parse_mode=html)
        else:
            await message.answer(f"{view_date}\n🎉 Added 🕝{hours} / ⭐️{int(point)}\n 🏄‍♂️{act}{category}", reply_markup=nav.not_today_menu(data.get('date')), parse_mode=html)
        await Focus.Q4.set()
    except Exception as ex:
        print(ex)
        await message.answer(f"Your duration is not invalid!\nPlease, type me new duration (example: 1,5 or 1:30)")
        await Focus.Q3.set()

@dp.callback_query_handler(text_contains= 'foc_')       
@dp.callback_query_handler(text_contains= 'foc_', state=Focus.Q4)
async def answer_message(call: types.CallbackQuery, state: FSMContext):
    if call.data== 'foc_del':
        data = await state.get_data()
        act= data.get('action_name')
        point= data.get('points')
        hour= data.get('hour')
        category=  data.get('category').split('_')[0]
        date_del= data.get('date')
        db.del_focus(user_id=call.message.chat.id, action=act, date=date_del, category=category)
        category= f" /🚦{category} useful"
        await call.message.answer(f"🚮 Deleted 🕝{hour} / ⭐️{int(point)}\n{act}{category}", reply_markup=nav.add_button, parse_mode=html)
        await state.finish()
    if call.data== 'foc_add':
        messages= ""
    
        if len(db.inf_about_action(user_id=call.message.chat.id)) == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
    
        await call.message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=call.message.chat.id), parse_mode=html)
        await Focus.Q1.set()

@dp.callback_query_handler(text_contains= 'tod_')       
@dp.callback_query_handler(text_contains= 'tod_', state=Focus.Q4)
async def answer_message(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'tod_today':
        await state.update_data(date=None)
        messages= ""
    
        if len(db.inf_about_action(user_id=call.message.chat.id)) == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
    
        await call.message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=call.message.chat.id), parse_mode=html)
        await Focus.Q1.set()
    if call.data == 'tod_del':
        data = await state.get_data()
        act= data.get('action_name')
        point= data.get('points')
        hour= data.get('hour')
        category=  data.get('category').split('_')[0]
        date_del= data.get('date')
        db.del_focus(user_id=call.message.chat.id, action=act, date=date_del, category=category)
        category= f" /🚦{category} useful"
        await call.message.answer(f"🚮 Deleted 🕝{hour} / ⭐️{int(point)}\n{act}{category}", reply_markup=nav.add_button, parse_mode=html)
        await state.finish()
    else:
        dt= call.data.split('_')[2]
        await state.update_data(date=dt)
        messages= ""
    
        if len(db.inf_about_action(user_id=call.message.chat.id)) == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
    
        await call.message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=call.message.chat.id), parse_mode=html)
        await Focus.Q1.set()










@dp.message_handler(commands=['stat'], state=Focus.all_states)
@dp.message_handler(commands=['stat'])
async def start_message(message: types.Message, state: FSMContext):
    await state.finish()
    actions= []
    _date= date.today()
    view_date= _date.strftime('%a, %d.%m')
    result= db.stat_today(user_id=message.chat.id, date= _date)
    messages=  get_stat_by_action(stat_list=result, actions_list=actions, week=True)
    await message.answer(f"🗓 {view_date}{messages}", reply_markup=nav.stat_menu(day='today', split='by actions', list_actions=[]), parse_mode=html)
                         
@dp.callback_query_handler(text_contains= 'stat_')
async def answer_message(call: types.CallbackQuery, state: FSMContext):
    data= await state.get_data()
    actions= data.get('actions')
    day=''
    split=''
    if actions == None: 
        actions= []
    if call.data == 'stat_today_by actions' or call.data == 'stat_today_by records' or call.data == 'stat_week_by day_':
        day='week'
        split= 'by actions'
        first_date= date.today()- timedelta(days= date.today().weekday())
        second_date= first_date + timedelta(weeks=1)
        view_date=f"Week {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
        result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
        messages=get_stat_by_action(stat_list=result, actions_list=actions, week=True)
    elif call.data == 'stat_week_by actions' or call.data == 'stat_week_by day' or call.data == 'stat_month_by week_':
        day='month'
        split= 'by actions'
        first_date= date(year=date.today().year, month=date.today().month, day=1)#.today()- timedelta(days= date.today().weekday())
        days_in_month = calendar.monthrange(year=date.today().year, month=date.today().month)[1]
        second_date= first_date + timedelta(days=days_in_month)
        view_date=f"Month {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
        result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
        messages=get_stat_by_action(stat_list=result, actions_list=actions)
    elif call.data == 'stat_month_by actions'or call.data == 'stat_month_by week' or call.data == 'stat_all_by week_':
        day='all'
        split= 'by actions'
        old= db.first_log(call.message.chat.id)[0].split('-')
        first_date=  date(year=int(old[0]), month=int(old[1]), day=int(old[2])) 
        second_date= date.today()
        view_date=f"All time {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
        result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=(second_date+timedelta(1)))
        messages=get_stat_by_action(stat_list=result, actions_list=actions)
    elif call.data == 'stat_all_by actions' or call.data == 'stat_all_by week' or call.data == 'stat_today_by records_':
        day='today'
        split= 'by actions'
        _date= date.today()
        view_date=_date.strftime('%a, %d.%m')
        result= db.stat_today(user_id=call.message.chat.id, date= _date)
        messages=  get_stat_by_action(stat_list=result, actions_list=actions, week=True)
    
    
    elif call.data == 'stat_today_by actions_':
        day='today'
        split= 'by records'
        _date= date.today()
        view_date=_date.strftime('%a, %d.%m')
        result= db.stat_today(call.message.chat.id, date= _date)
        messages= get_stat_by_records(stat_list=result, actions_list=actions)
        
    elif call.data == 'stat_week_by actions_':
        day='week'
        split= 'by day'
        first_date= date.today() - timedelta(7)
        second_date= date.today() + timedelta(1)
        view_date= f"Week {first_date.strftime('%d.%m')} — {date.today().strftime('%d.%m')}"
        messages=get_stat_by_day(call.message.chat.id, actions, first_date, second_date)
    elif call.data == 'stat_month_by actions_':
        day='month'
        split= 'by week'
        first_date= date.today()- timedelta(days= date.today().weekday()) - timedelta(weeks=4)
        second_date= date.today() + timedelta(days=(6-date.today().weekday()))
        view_date= f"Month {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
        messages= get_stat_by_week(user_id=call.message.chat.id, actions_list=actions, first_date=first_date, second_date=second_date)
    elif call.data == 'stat_all_by actions_':
        day='all'
        split= 'by week'
        old= db.first_log(call.message.chat.id)[0].split('-')
        old_date= date(year=int(old[0]), month=int(old[1]), day=int(old[2]))
        first_date=  old_date - timedelta(days=old_date.weekday())
        second_date= date.today() + timedelta(days=(7-date.today().weekday()))
        view_date= f"All time {first_date.strftime('%d.%m')} — {(second_date - timedelta(1)).strftime('%d.%m')}"
        messages= get_stat_by_week(user_id=call.message.chat.id, actions_list=actions, first_date=first_date, second_date=second_date)
    await call.message.edit_text(text=f"🗓 {view_date}{messages}", reply_markup=nav.stat_menu(day=day, split=split, list_actions=actions), parse_mode=html)
    
@dp.callback_query_handler(text_contains= 'act_')
async def answer_message(call: types.CallbackQuery, state: FSMContext):
    data= await state.get_data()
    actions= data.get('actions')
    if actions == None:
        actions= []
    day_=call.data.split('_')[1]
    split_= call.data.split('_')[2]
    await state.update_data(day=day_)
    await state.update_data(split=split_)
    await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=nav.choose_action_menu(list_actions=actions))

@dp.callback_query_handler(text_contains= 'choose_')
async def answer_message(call: types.CallbackQuery, state: FSMContext):
    data= await state.get_data()
    actions_list= []
    if data.get('actions') != None:
        for act in data.get('actions'):
            actions_list.append(act)
    if call.data == 'choose_done':
        if data.get('split') == 'by actions':
            if data.get('day') == 'today':
                _date= date.today()
                view_date= _date.strftime("%d.%m")
                result= db.stat_today(user_id=call.message.chat.id, date= _date)
                messages=  get_stat_by_action(stat_list=result, actions_list=actions_list, week=True)
            if data.get('day') == 'week':
                first_date= date.today()- timedelta(days= date.today().weekday())
                second_date= first_date + timedelta(weeks=1)
                view_date=f"Week {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
                result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
                messages=get_stat_by_action(stat_list=result, actions_list=actions_list, week=True)
            if data.get('day') == 'month':
                first_date= date(year=date.today().year, month=date.today().month, day=1)#.today()- timedelta(days= date.today().weekday())
                days_in_month = calendar.monthrange(year=date.today().year, month=date.today().month)[1]
                second_date= first_date + timedelta(days=days_in_month)
                view_date=f"Month {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
                result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
                messages=get_stat_by_action(stat_list=result, actions_list=actions_list)
            if data.get('day') == 'all':
                old= db.first_log(call.message.chat.id)[0].split('-')
                first_date=  date(year=int(old[0]), month=int(old[1]), day=int(old[2])) 
                second_date= date.today()
                view_date=f"All time {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
                result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
                messages=get_stat_by_action(stat_list=result, actions_list=actions_list)
        else:
            if data.get('day') == 'today':
                _date= date.today()
                view_date=_date.strftime('%a, %d.%m')
                result= db.stat_today(call.message.chat.id, date= _date)
                messages= get_stat_by_records(stat_list=result, actions_list=actions_list)
            if data.get('day') == 'week':
                first_date= date.today() - timedelta(weeks=1)
                second_date= date.today()
                view_date= f"{first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
                
            if data.get('day') == 'month':
                first_date= date.today()- timedelta(days= date.today().weekday()) - timedelta(weeks=4)
                second_date= date.today() + timedelta(days=(6-date.today().weekday()))
                view_date= f"Month {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
                messages= get_stat_by_week(user_id=call.message.chat.id, actions_list=actions_list, first_date=first_date, second_date=second_date)
            if data.get('day') == 'all':
                old= db.first_log(call.message.chat.id)[0].split('-')
                old_date= date(year=int(old[0]), month=int(old[1]), day=int(old[2]))
                first_date=  old_date - timedelta(days=old_date.weekday())
                second_date= date.today() + timedelta(days=(7-date.today().weekday()))
                view_date= f"Week {first_date.strftime('%d.%m')} — {(second_date - timedelta(1)).strftime('%d.%m')}"
                messages= get_stat_by_week(user_id=call.message.chat.id, actions_list=actions_list, first_date=first_date, second_date=second_date)
        await call.message.edit_text(f"🗓 {view_date}{messages}", reply_markup=nav.stat_menu(day=data.get('day'), split=data.get('split'), list_actions=actions_list), parse_mode=html)
    
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
    for user_id in db.user_info_id():
        await dp.bot.send_message(chat_id=user_id, text=f"🎉 It was a great week!\nYou got ⭐️ <b>{int(db.get_points_atweek(user_id)[0])}</b> for this 7 days", parse_mode=html)

async def every_day():
    for user_id in db.user_info_id():
        if db.stat_today(user_id=user_id, date=date.today()) != None:
            await dp.bot.send_message(chat_id=user_id, text=f"🤜🤛 Just do it! You have shock mode 🔥21 days. Don't lose it!", parse_mode=html, reply_markup=nav.log_button)



async def scheduler():
    aioschedule.every().monday.at("10:00").do(every_mon)
    
    #aioschedule.every().minute.do(every_mon)
    aioschedule.every().day.at("12:00").do(every_day)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def notification(_):
    asyncio.create_task(scheduler())




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=notification)