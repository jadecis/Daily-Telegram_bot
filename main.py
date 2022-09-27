from db import Database
import config as cfg
import keyboard as nav
from datetime import datetime, time, timedelta, date
import calendar
import asyncio
import aioschedule
from math import floor
import uuid

import logging
import aiogram
from aiogram import Bot, executor, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

bot = Bot(token=cfg.TOKEN)
logging.basicConfig(level=logging.INFO)
dp= Dispatcher(bot=bot, storage=MemoryStorage())
db= Database('database.db')

class Focus(StatesGroup):
    Q1= State()
    Q2= State()
    Q3= State()
    Q4= State()
    Q5= State()
    
html= types.ParseMode.HTML#<- &lt; >- &gt; &- &amp; 
mark= types.ParseMode.MARKDOWN
v2= types.ParseMode.MARKDOWN_V2

def get_stat_by_action(stat_list, user_id, actions_list, week=False ):
    points = {}
    hours = {}
    categories =True
    decimal= 1 if week is False else 0.1
    count_skip= db.user_info(user_id)[2]
    user_cat=db.get_user_cat(user_id)
    star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
    if (count_skip > 0 and count_skip < 8) and star is True:
        categories= True
        zero_point= True
    elif count_skip == 0:
        categories= True
        zero_point= False
    else:
        categories =False
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
                if type(hours_name) != str: hours_name= int(hours_name) if week is False else (floor((hours_name- int(hours_name)) * 10))/10 + int(hours_name)
                point= 0 if zero_point is True else int(points[name])
                message+= f"\n{name} 🕝{hours_name}/ ⭐️{point}"
            hours_name_total= f'&lt;{decimal}' if (total_hours > 0) and (total_hours < decimal) else total_hours
            totalpoint= 0 if zero_point is True else int(total_points)
            if type(hours_name_total) == float: hours_name_total= int(total_hours) if week is False else (floor((total_hours- int(total_hours)) * 10))/10 + int(total_hours)
            message+= f"\n\n<b>Total</b>: 🕝{hours_name_total}/ ⭐️{totalpoint}"
            return message
        else: return "\nYou haven't been active or you haven't been active this action during this interval of time"
    else:
        if len(hours) != 0:
            for name in hours:
                total_hours+=hours[name]
                hours_name= f'&lt;{decimal}' if hours[name] > 0 and hours[name] < decimal else hours[name]
                if type(hours_name) != str: hours_name= int(hours_name) if week is False else (floor((hours_name- int(hours_name)) * 10))/10 + int(hours_name)
                message+= f"\n{name} 🕝{hours_name}"
            hours_name_total= f'&lt;{decimal}' if (total_hours > 0) and (total_hours < decimal) else total_hours
            if type(hours_name_total) == float: hours_name_total= int(total_hours) if week is False else (floor((total_hours- int(total_hours)) * 10))/10 + int(total_hours)
            message+= f"\n\n<b>Total</b>: 🕝{hours_name_total}"
            return message
        else: return "\nYou haven't been active or you haven't been active this action during this interval of time"
    
def get_stat_by_week(user_id, actions_list, first_date, second_date):
    message= ""
    count_skip= db.user_info(user_id)[2]
    user_cat=db.get_user_cat(user_id)
    zero_point= False
    star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
    if (count_skip > 0 and count_skip < 8) and star is True:
        categories= True
        zero_point= True
    elif count_skip == 0:
        categories= True
        zero_point= False
    else:
        categories =False
    top= {}
    prise=''
    while first_date < second_date:
        total_hours= 0.0
        total_points= 0.0
        result= db.stat_by_interval(user_id=user_id, first_date=first_date, second_date=first_date+ timedelta(weeks=1))
        #if len(result) != 0: return "\nYou haven't been active or you haven't been active this action during this interval of time"
        if len(actions_list) != 0:
            for stat in result:
                if list(actions_list).__contains__(stat[0]):
                    total_hours+=stat[1]
                    total_points+= stat[2]
        else:
            for stat in result:
                total_hours+=stat[1]
                total_points+= stat[2]
        top[first_date]= {'hour' : total_hours, 'point' : total_points}
        first_date += timedelta(weeks=1)
    sort_top= sorted(top.items(), key=lambda x: x[1].get('point'), reverse=True)
    for key in top:
        prise= ""
        point= 0 if zero_point is True else int(top[key]['point'])
        if point != 0:
            if sort_top[0][0] == key and sort_top[0][1].get('point') == top[key].get('point') and sort_top[0][1].get('point') != 0:
                prise= "🥇" 
            elif sort_top[1][0] == key and sort_top[1][1].get('point') == top[key].get('point') and sort_top[1][1].get('point') != 0:
                prise= "🥈"
            elif sort_top[2][0] == key and sort_top[2][1].get('point') == top[key].get('point') and sort_top[2][1].get('point') != 0:
                prise= "🥉"
            else:
                prise= ""
        hours= '&lt;1' if (top[key]['hour'] > 0) and (top[key]['hour'] < 1) else int(top[key]['hour'])
        if categories is True:
            
            message+=f"\n{key.strftime('%d-%b')} 🕝{hours}/ ⭐️{point} {prise}"
        else:
            message+=f"\n{key.strftime('%d-%b')} 🕝{hours} {prise}"
               
    return message
            
def get_stat_by_records(stat_list, actions_list, user_id):
    message=""
    count_skip= db.user_info(user_id)[2]
    user_cat=db.get_user_cat(user_id)
    zero_point= False
    star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
    if (count_skip > 0 and count_skip < 8) and star is True:
        categories= True
        zero_point= True
    elif count_skip == 0:
        categories= True
        zero_point= False
    else:
        categories =False
    if len(actions_list) != 0:  
        for stat in stat_list:
            if list(actions_list).__contains__(stat[0]):
                duration= f'({stat[4]})' if stat[4] != None else ""
                hour= '&lt;0.1' if stat[1] > 0 and stat[1] < 0.1 else (floor((stat[1]- int(stat[1])) * 10))/10 + int(stat[1])
                if categories is True:
                    point= 0 if zero_point is True else int(stat[2])
                    message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} / ⭐️{point} {duration}"
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
                hour= '&lt;0.1' if stat[1] > 0 and stat[1] < 0.1 else (floor((stat[1]- int(stat[1])) * 10))/10 + int(stat[1])
                if categories is True:
                    point= 0 if zero_point is True else int(stat[2])
                    message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} / ⭐️{point} {duration}"
                else:

                    message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} {duration}"
            return message
        
def get_stat_by_day(user_id, action_list, first_date, second_date):
    message= ""
    count_skip= db.user_info(user_id)[2]
    user_cat=db.get_user_cat(user_id)
    zero_point= False
    star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
    if 8 > count_skip > 0 and star is True:
        categories= True
        zero_point= True
    elif count_skip == 0:
        categories= True
        zero_point= False
    else:
        categories =False
    top ={}
    prise=""
    while first_date < second_date:
        result= db.stat_today(user_id=user_id, date=first_date)
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
        top[first_date]= {'hour' : total_hours, 'point' : total_points}
        first_date += timedelta(1)
    sort_top= sorted(top.items(), key=lambda x: x[1].get('point'), reverse=True)
    for key in top:
        prise= ""
        point= 0 if zero_point is True else int(top[key]['point'])
        if point != 0:
            if sort_top[0][0] == key and sort_top[0][1].get('point') == top[key].get('point') and top[key].get('point') != 0:
                prise= "🥇" 
            elif sort_top[1][0] == key and sort_top[1][1].get('point') == top[key].get('point') and top[key].get('point') != 0:
                prise= "🥈"
            elif sort_top[2][0] == key and sort_top[2][1].get('point') == top[key].get('point') and top[key].get('point') != 0:
                prise= "🥉"
            else:
                prise= ""
        hours= '&lt;0.1' if top[key]['hour'] > 0 and top[key]['hour'] < 0.1 else (floor((top[key]['hour']-int(top[key]['hour'])) * 10))/10 +int(top[key]['hour'])
        if categories is True:
            message+= f"\n{key.strftime('%a')} 🕝{hours} / ⭐️{point} {prise}"
        else:
            message+= f"\n{key.strftime('%a')} 🕝{hours} {prise}"
        
    return message

def stat_friend(i,friends, user_id):
    user_id_friend= int(friends[i])

    count_skip= db.user_info(user_id)[2]
    user_cat=db.get_user_cat(user_id)
    zero_point= False
    star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
    if (count_skip > 0 and count_skip < 8) and star is True:
        categories= True
        zero_point= True
    elif count_skip == 0:
        categories= True
        zero_point= False
    else:
        categories =False
    
    
    today= date.today()
    monday= date.today()- timedelta(days= date.today().weekday())
    first_day= date(year=date.today().year, month=date.today().month, day=1)
    days_in_month = calendar.monthrange(year=date.today().year, month=date.today().month)[1]
    old= db.first_log(user_id_friend)[0].split('-') if db.first_log(user_id_friend)[0] != None else date.today().strftime('%Y-%m-%d').split('-')
    old_date_friend=  date(year=int(old[0]), month=int(old[1]), day=int(old[2]))
    old= db.first_log(user_id)[0].split('-') if db.first_log(user_id)[0] != None else date.today().strftime('%Y-%m-%d').split('-')
    old_date=date(year=int(old[0]), month=int(old[1]), day=int(old[2]))
    week= [monday, monday+timedelta(days=6)]
    month= [first_day, first_day+timedelta(days=days_in_month)- timedelta(days=1)]
    all_friend= [old_date_friend, today]
    all= [old_date, today]

    today_friend=db.stat_short_today(user_id=user_id_friend) if db.stat_short_today(user_id=user_id_friend) != tuple([None, None]) else [0,0]
    today_me=db.stat_short_today(user_id=user_id) if db.stat_short_today(user_id=user_id) != tuple([None, None]) else [0,0]

    stat_week_friend= db.get_short_stat(user_id=user_id_friend, first_date= week[0], second_date= week[1]) if db.get_short_stat(user_id=user_id_friend, first_date= week[0], second_date= week[1]) != tuple([None, None]) else [0,0]
    stat_week= db.get_short_stat(user_id=user_id, first_date= week[0], second_date= week[1]) if db.get_short_stat(user_id=user_id, first_date= week[0], second_date= week[1]) != tuple([None, None]) else [0,0]
    
    stat_month_friend= db.get_short_stat(user_id=user_id_friend, first_date= month[0], second_date= month[1]) if db.get_short_stat(user_id=user_id_friend, first_date= month[0], second_date= month[1]) != tuple([None, None]) else [0,0]
    stat_month= db.get_short_stat(user_id=user_id, first_date= month[0], second_date= month[1]) if db.get_short_stat(user_id=user_id, first_date= month[0], second_date= month[1]) != tuple([None, None]) else [0,0]

    stat_all_friend= db.get_short_stat(user_id=user_id_friend, first_date= all_friend[0], second_date= all_friend[1]) if db.get_short_stat(user_id=user_id_friend, first_date= all_friend[0], second_date= all_friend[1]) != tuple([None, None]) else [0,0]
    stat_all= db.get_short_stat(user_id=user_id, first_date= all[0], second_date= all[1]) if db.get_short_stat(user_id=user_id, first_date= all[0], second_date= all[1]) != tuple([None, None]) else [0,0]
    
    today_hour_fr= '&lt;0.1' if today_friend[0] > 0 and today_friend[0] < 0.1 else (floor((today_friend[0]-int(today_friend[0])) * 10))/10 + int(today_friend[0])
    today_hour_me= '&lt;0.1' if today_me[0] > 0 and today_me[0] < 0.1 else (floor((today_me[0]- int(today_me[0])) * 10))/10+ int(today_me[0])
    
    week_fr= '&lt;0.1' if stat_week_friend[0] > 0 and stat_week_friend[0] < 0.1 else (floor((stat_week_friend[0]-int(stat_week_friend[0])) * 10))/10+ int(stat_week_friend[0])
    week_me= '&lt;0.1' if stat_week[0] > 0 and stat_week[0] < 0.1 else (floor((stat_week[0]-int(stat_week[0])) * 10))/10+ int(stat_week[0])

    month_fr= '&lt;1' if stat_month_friend[0] > 0 and stat_month_friend[0] < 1 else int(stat_month_friend[0])
    month_me= '&lt;1' if stat_month[0] > 0 and stat_month[0] < 1 else int(stat_month[0])
    
    all_fr= '&lt;1' if stat_all_friend[0] > 0 and stat_all_friend[0] < 1 else int(stat_all_friend[0])
    all_me= '&lt;1' if stat_all[0] > 0 and stat_all[0] < 1 else int(stat_all[0])
    
    if categories is True:
        if zero_point is True:   
            message=f"""
🙋 @{db.get_user_name(user_id_friend)[0]}
Day 🕝{today_hour_fr} / ⭐️{int(today_friend[1])} (you: 🕝{today_hour_me} / ⭐️{int(today_me[1])})
Week 🕝{week_fr} / ⭐️{int(stat_week_friend[1])} (you: 🕝{week_me} / ⭐️{int(stat_week[1])})
Month 🕝{month_fr} / ⭐️{int(stat_month_friend[1])} (you: 🕝{month_me} / ⭐️{int(stat_month[1])})
All 🕝{all_fr} / ⭐️{int(stat_all_friend[1])} (you: 🕝{all_me} / ⭐️{int(stat_all[1])})
"""
        else:
            message=f"""
🙋 @{db.get_user_name(user_id_friend)[0]}
Day 🕝{today_hour_fr} / ⭐️{int(today_friend[1])} (you: 🕝{today_hour_me} / ⭐️0)
Week 🕝{week_fr} / ⭐️{int(stat_week_friend[1])} (you: 🕝{week_me} / ⭐️0)
Month 🕝{month_fr} / ⭐️{int(stat_month_friend[1])} (you: 🕝{month_me} / ⭐️0)
All 🕝{all_fr} / ⭐️{int(stat_all_friend[1])} (you: 🕝{all_me} / ⭐️0)
"""
    else:
                message=f"""
🙋 @{db.get_user_name(user_id_friend)[0]}
Day 🕝{today_hour_fr} (you: 🕝{today_hour_me})
Week 🕝{week_fr} (you: 🕝{week_me})
Month 🕝{month_fr} (you: 🕝{month_me})
All 🕝{all_fr} (you: 🕝{all_me})
"""
    return message



@dp.message_handler(commands=['start'], state=Focus.all_states)
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message, state: FSMContext):
    await state.finish()
    if db.user_info(user_id=message.chat.id) == None:
        db.add_user(user_id=message.chat.id, user_name=message.from_user.username)
    if db.get_user_name(user_id=message.chat.id)[0] == None:
        db.up_name(user_id=message.chat.id, user_name=message.from_user.username)
    await message.answer(f"Hello! This is a bot for tracking your daily activities. What is your goal?", reply_markup=nav.main_menu)

@dp.message_handler(commands=['s'], state=Focus.all_states)
@dp.message_handler(commands=['s'])
async def s_message(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"New keyboard", reply_markup=nav.menu_markup)
                         
                         
@dp.callback_query_handler(text= 'start')
async def answer_message(call: types.CallbackQuery):
    await call.message.answer(
    f"Great! This bot helps you to record how much time you spent on various activities. The bot will store and show you how productive you were in different days, weeks and months.\n\nNow let's record your first activity!", reply_markup=nav.record_button) 
    
@dp.message_handler(commands=['friends'], state=Focus.all_states)
@dp.message_handler(commands=['friends'])
async def friends_message(message: types.Message, state: FSMContext):
    await state.finish()
    if db.user_info(user_id=message.chat.id)[3] == None or db.user_info(user_id=message.chat.id)[3]== '':
        await message.answer(f"You don't have any friends yet. Add them!", reply_markup=nav.add_friends_button)
    else: 
        friends= db.get_friends(user_id= message.chat.id)[0].split(',')
        await message.answer(text=stat_friend(i=0, friends=friends, user_id=message.chat.id), reply_markup=nav.next_menu(i=0, user_id=message.chat.id), parse_mode=html)

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
    if db.get_count_logs(message.chat.id)[0] == 0:
        messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
    else:
        messages="Select or type <b>activity</b>🏄‍♂️"
    await message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=message.chat.id), parse_mode=html)
    await Focus.Q1.set()

@dp.message_handler(commands=['stat'], state=Focus.all_states)
@dp.message_handler(commands=['stat'])
async def start_message(message: types.Message, state: FSMContext):
    await state.finish()
    if db.user_info(user_id=message.chat.id) == None:
        db.add_user(user_id=message.chat.id, user_name=message.from_user.username)
    if db.get_user_name(user_id=message.chat.id)[0] == None:
        db.up_name(user_id=message.chat.id, user_name=message.from_user.username)
    actions= []
    _date= date.today()
    view_date= _date.strftime('%a, %d.%m')
    result= db.stat_today(user_id=message.chat.id, date= _date)
    
    messages=  get_stat_by_action(stat_list=result, actions_list=actions, week=True, user_id=message.chat.id)
    await message.answer(f"🗓 {view_date}{messages}", reply_markup=nav.stat_menu(day='today', split='by actions', list_actions=[]), parse_mode=html)

@dp.message_handler(content_types=['text'], state= Focus.Q4)
@dp.message_handler(content_types=['text'], state= Focus.Q2)
@dp.message_handler(content_types=['text'])
async def text_answer(message: types.Message, state: FSMContext):
    if message.text == 'Record activity':
        await state.finish()
        try:
            float(message.text[7:])
            await state.update_data(date=message.text[7:])
        except  Exception as ex:
            pass
            
        messages= ""
        if db.get_count_logs(message.chat.id)[0] == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
        await message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=message.chat.id), parse_mode=html)
        await Focus.Q1.set()
    elif message.text == 'Show statistics':
        await state.finish()
        if db.user_info(user_id=message.chat.id) == None:
            db.add_user(user_id=message.chat.id, user_name=message.from_user.username)
        if db.get_user_name(user_id=message.chat.id)[0] == None:
            db.up_name(user_id=message.chat.id, user_name=message.from_user.username)
        actions= []
        _date= date.today()
        view_date= _date.strftime('%a, %d.%m')
        result= db.stat_today(user_id=message.chat.id, date= _date)
        messages=  get_stat_by_action(stat_list=result, actions_list=actions, week=True, user_id=message.chat.id)
        await message.answer(f"🗓 {view_date}{messages}", reply_markup=nav.stat_menu(day='today', split='by actions', list_actions=[]), parse_mode=html)
    else:
        await message.delete()

@dp.callback_query_handler(text_contains= 'next_')
async def next_answer(call: types.CallbackQuery, state: FSMContext):
    i = int(call.data[5:])
    count_fr= len(db.get_friends(call.message.chat.id)[0].split(','))-2
    i=0 if i== count_fr else i+1
    friends= db.get_friends(user_id= call.message.chat.id)[0].split(',')
    await call.message.edit_text(text=stat_friend(i=i, friends=friends, user_id=call.message.chat.id), reply_markup=nav.next_menu(i=i, user_id=call.message.chat.id), parse_mode=html)
        
@dp.callback_query_handler(text= 'friend')
async def friend_answer(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Write a friend's username (example: '@my_best_friend')")
    await Focus.Q5.set()
    
@dp.message_handler(content_types=['text'], state=Focus.Q5)
async def q5_answer(message: types.Message, state: FSMContext):
    if message.text == 'Record activity':
        await state.finish()
        try:
            float(message.text[7:])
            await state.update_data(date=message.text[7:])
        except  Exception as ex:
            pass
            
        messages= ""
        if db.get_count_logs(message.chat.id)[0] == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
        await message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=message.chat.id), parse_mode=html)
        await Focus.Q1.set()
    elif message.text == 'Show statistics':
        await state.finish()
        if db.user_info(user_id=message.chat.id) == None:
            db.add_user(user_id=message.chat.id, user_name=message.from_user.username)
        if db.get_user_name(user_id=message.chat.id)[0] == None:
            db.up_name(user_id=message.chat.id, user_name=message.from_user.username)
        actions= []
        _date= date.today()
        view_date= _date.strftime('%a, %d.%m')
        result= db.stat_today(user_id=message.chat.id, date= _date)
        messages=  get_stat_by_action(stat_list=result, actions_list=actions, week=True, user_id=message.chat.id)
        await message.answer(f"🗓 {view_date}{messages}", reply_markup=nav.stat_menu(day='today', split='by actions', list_actions=[]), parse_mode=html)
    else:
        user_id= db.find_id(user_name=message.text[1:])
        list_friends= []
        if  db.get_friends(user_id=message.chat.id)[0]!=None:
            list_friends = db.get_friends(user_id=message.chat.id)[0].split(',')
        if user_id == None:
            await message.answer(f"Friend not found!\nPlease, write username who using this bot!!!")
            await Focus.Q5.set()
        elif user_id[0] == message.chat.id:
            await message.answer(f"You can't add yourself!\nPlease, write username other friend!")
        elif list_friends.__contains__(str(user_id[0])):
            await message.answer(f"Friend have already been added!!!\nPlease, write username other friend!")
            await Focus.Q5.set()
        else:
            await message.answer(f"✅ Ready! {message.text} has received a friend request and needs to confirm it. After confirmation, the friend will appear in the friends section", reply_markup=nav.friends_menu)
            await bot.send_message(chat_id=user_id[0], text=f"🙋 @{message.chat.username} wants to add you to friends. If you agree, you will be able to see each other's stats.", reply_markup=nav.add_friends_menu(user_name=message.chat.username))
            await state.finish()
        
@dp.callback_query_handler(text_contains= 'friend_')
async def friend_answer(call: types.CallbackQuery, state: FSMContext):
    if call.data== 'friend_show':
        await state.finish()
        if db.user_info(user_id=call.message.chat.id)[3] == None:
            await call.message.answer(f"You don't have any friends yet. Add them!", reply_markup=nav.add_friends_button)
        else:
            friends= db.get_friends(user_id= call.message.chat.id)[0].split(',')
            await call.message.answer(text=stat_friend(i=0, friends=friends, user_id=call.message.chat.id), reply_markup=nav.next_menu(i=0, user_id=call.message.chat.id), parse_mode=html)
    elif call.data== 'friend_add':
        await call.message.edit_text("Write a friend's username (example: '@my_best_friend')")
        await Focus.Q5.set()

@dp.callback_query_handler(text_contains= 'to_')
async def to_answer(call: types.CallbackQuery, state: FSMContext):
    user_name= call.data.split('%')[1]
    user_id= int(db.find_id(user_name=user_name)[0])
    if call.data.__contains__('to_add'):
        friends= db.get_friends(call.message.chat.id)[0] if db.get_friends(call.message.chat.id)[0] !=None else ""
        _friends= db.get_friends(user_id)[0] if db.get_friends(user_id)[0] !=None else ""
        friends+=f"{user_id},"
        _friends+=f"{call.message.chat.id},"
        db.add_friend(user_id=call.message.chat.id, friend_id= f"{friends}")
        db.add_friend(user_id=user_id, friend_id= f"{_friends}")
        await call.message.answer(text=f"💁 @{user_name} is now your friend. You can see his data in the section /friends", reply_markup=nav.rej_markup(user_id))
        await bot.send_message(chat_id=user_id, text=f"🎉 @{call.message.chat.username} has accepted your friend offer! Now you can see his stats!", reply_markup=nav.show_friend_button)
    if call.data.__contains__('to_rej'):
        await call.message.answer(text=f"🙅 You rejected the application of @{user_name}", reply_markup=nav.add_markup(user_id))
    await state.finish()
    
@dp.callback_query_handler(text_contains= 'change_')
async def change_answer(call: types.CallbackQuery, state: FSMContext):
    user_id= call.data.split('%')[1]
    user_name= db.get_user_name(user_id)[0]
    if call.data.__contains__('change_add'):
        friends= db.get_friends(call.message.chat.id)[0] if db.get_friends(call.message.chat.id)[0] !=None else ""
        _friends= db.get_friends(user_id)[0] if db.get_friends(user_id)[0] !=None else ""
        friends+=f"{user_id},"
        _friends+=f"{call.message.chat.id},"
        db.add_friend(user_id=call.message.chat.id, friend_id= f"{friends}")
        db.add_friend(user_id=user_id, friend_id= f"{_friends}")
        await call.message.answer(text=f"💁 @{user_name} is now your friend. You can see his data in the section /friends")
        await bot.send_message(chat_id=user_id, text=f"🎉 @{call.message.chat.username} has accepted your friend offer! Now you can see his stats!", reply_markup=nav.show_friend_button)
    if call.data.__contains__('change_rej'):
        friends= db.get_friends(call.message.chat.id)[0]
        _friends= db.get_friends(user_id)[0]
        db.add_friend(user_id=call.message.chat.id, friend_id= f"{friends.replace(f'{user_id},', '')}")
        db.add_friend(user_id=user_id, friend_id= f"{_friends.replace(f'{call.message.chat.id},', '')}")
        await call.message.answer(text=f"🙅 You rejected the application of @{user_name}")
    await state.finish()


   
@dp.callback_query_handler(text= 'record')
async def record_answer(call: types.CallbackQuery, state: FSMContext):
    messages= ""

    if db.get_count_logs(user_id=call.message.chat.id)[0] == 0:
        messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
    else:
        messages="Select or type <b>activity</b>🏄‍♂️"
    
    await call.message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=call.message.chat.id), parse_mode=html)
    await Focus.Q1.set()

@dp.message_handler(content_types=['text'], state=Focus.Q1)
async def q1_answer(message: types.Message, state: FSMContext):
    if message.text == 'Record activity':
        await state.finish()
        try:
            float(message.text[7:])
            await state.update_data(date=message.text[7:])
        except  Exception as ex:
            pass
            
        messages= ""
        if db.get_count_logs(message.chat.id)[0] == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
        await message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=message.chat.id), parse_mode=html)
        await Focus.Q1.set()
    elif message.text == 'Show statistics':
        await state.finish()
        if db.user_info(user_id=message.chat.id) == None:
            db.add_user(user_id=message.chat.id, user_name=message.from_user.username)
        if db.get_user_name(user_id=message.chat.id)[0] == None:
            db.up_name(user_id=message.chat.id, user_name=message.from_user.username)
        actions= []
        _date= date.today()
        view_date= _date.strftime('%a, %d.%m')
        result= db.stat_today(user_id=message.chat.id, date= _date)
        messages=  get_stat_by_action(stat_list=result, actions_list=actions, week=True, user_id=message.chat.id)
        await message.answer(f"🗓 {view_date}{messages}", reply_markup=nav.stat_menu(day='today', split='by actions', list_actions=[]), parse_mode=html)
    else:
        act= message.text
        res=db.last_actions(user_id=message.chat.id)
        await state.update_data(action_name=act)
        for act_res in res:
            act_res[0].lower()
            if act_res[0].lower()== act.lower():
                await state.update_data(action_name=act_res[0])
                act= act_res[0]
                await Focus.Q2.set()
                break
        skip_inf= int(db.user_info(user_id=message.chat.id)[2])
        user_cat=db.get_user_cat(message.chat.id)
        star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
        try:
            if (skip_inf >= 8 and star is True) or (skip_inf >= 4 and star is False):
                await message.edit_text(f"🏄‍♂️ {act}\n\nStart recording or have you already performed the action?", reply_markup=nav.log_menu, parse_mode=html)
            else:
                await message.answer(f"🏄‍♂️{act}\nSelect the level of 🚦<b>usefulness</b> of activity", reply_markup=nav.categories_menu(), parse_mode=html)
            await Focus.Q2.set()
        except aiogram.utils.exceptions.CantParseEntities:
            await message.answer(f"Please, don't type this symbol: '<, >, &' ")
            await Focus.Q1.set()
    
@dp.callback_query_handler(text_contains= 'act_', state=Focus.Q1)
async def act_answer(call: types.CallbackQuery, state: FSMContext):
    act= call.data.split('_')[1]
    skip_inf= int(db.user_info(user_id=call.message.chat.id)[2])
    user_cat=db.get_user_cat(call.message.chat.id)
    star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
    try:
        if (skip_inf >= 8 and star is True) or (skip_inf >= 4 and star is False):
            await call.message.edit_text(f"🏄‍♂️ {act}\n\nStart recording or have you already performed the action?", reply_markup=nav.log_menu, parse_mode=html)
        else:
            await call.message.edit_text(f"🏄‍♂️{act}\n\nSelect the level of 🚦<b>usefulness</b> of activity", reply_markup=nav.categories_menu(), parse_mode=html)
        await state.update_data(action_name=act)
        await Focus.Q2.set()
    except aiogram.utils.exceptions.CantParseEntities:
        await call.message.answer(f"Please, don't type this symbol: '<, >, &' ")
        await Focus.Q1.set()
           
@dp.callback_query_handler(text_contains= 'cat_', state=Focus.Q2)
async def cat_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cat= call.data.replace('cat_', '')
    act= data.get('action_name')
    if cat== 'Skip':
        db.skip_user(call.message.chat.id)
        await call.message.edit_text(f"🏄‍♂️ {act}\n\nStart recording or have you already performed the action?", reply_markup=nav.log_menu, parse_mode=html)
    else:
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
    if call.data == "log_start":
        data = await state.get_data()
        start_date= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        category = '' if data.get('category') == None else f" /🚦{data.get('category').split('_')[0]} useful"
        act= data.get('action_name')
        await state.update_data(rec_date=start_date)
        await state.update_data(start_dur_date=start_date)
        await call.message.edit_text(f"⏳ Recording...\n 🏄‍♂️ {act}{category}\nMay the focus be with you! 🧘‍♂️", reply_markup=nav.record_menu)
        
@dp.callback_query_handler(text_contains= 'rec_', state=Focus.Q2)
async def rec_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cat= data.get('category').split('_')[0] if data.get('category') != None else ""
    category = '' if cat == "" else f" /🚦{cat.split('_')[0]} useful"
    
    act= data.get('action_name')
    if call.data== 'rec_stop':
        start_dur= datetime.strptime(data.get('start_dur_date'), '%Y-%m-%d %H:%M:%S')  
        stop_dur= datetime.now() if data.get('stop_dur_date') == None else data.get('stop_dur_date')
        
        start_date= datetime.strptime(data.get('rec_date'), '%Y-%m-%d %H:%M:%S') 
        stop_date= datetime.now()
        if data.get('time_stop') != None and data.get('resume') == None:
            time=float(data.get('time_stop'))
        elif data.get('time_stop') != None and data.get('resume') == True:
            time=float(data.get('time_stop')) + (stop_date- start_date).total_seconds() / 3600
        else:
            time= (stop_date- start_date).total_seconds() / 3600
        if cat == "":
            multi= 0
        else:
            multi= int(data.get('category').split('_')[1])
        point= multi * time
        hour= '&lt;0.1' if time < 0.1 and time > 0 else time
        if type(hour) == float:
            if hour == 1.2:
                hour= 1.2
            elif int(hour) >= 1:
                hour= (floor((hour- int(hour)) * 10))/10+ int(hour)
            else:
                hour=(floor(hour * 10))/10+ int(hour)
        duration= f"{start_dur.strftime('%H:%M')} - {stop_dur.strftime('%H:%M')}"
        key= str(uuid.uuid4())
        db.add_focus(user_id=call.message.chat.id, action=act, hour=time, date=date.today(), category=cat, point=point, duration=duration, key=key)
        count_skip= db.user_info(call.message.chat.id)[2]
        user_cat=db.get_user_cat(call.message.chat.id)
        star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
        if (count_skip > 0 and count_skip < 8) and star is True:
            messages=f"{duration}\n🎉 Added 🕝{hour} / ⭐️0\n🏄‍♂️ {act}{category}"
        elif count_skip == 0:
            messages=f"{duration}\n🎉 Added 🕝{hour} / ⭐️{int(point)}\n🏄‍♂️ {act}{category}"
        else:
            messages=f"{duration}\n🎉 Added 🕝{hour}\n🏄‍♂️ {act}{category}"
        await call.message.edit_text(f"{messages}", parse_mode=html, reply_markup=nav.focus_menu(key=key))
        if db.get_count_logs(user_id=call.message.chat.id)[0] == 1:
            await call.message.answer(f"It's your first focus!🔥 Good job!\nUse the buttons below for record activity and show statistics", reply_markup= nav.menu_markup, parse_mode=html)
        await state.finish()
    if call.data== 'rec_pause':
        start_date= datetime.strptime(data.get('rec_date'), '%Y-%m-%d %H:%M:%S') 
        stop_date= datetime.now()
        time= (stop_date- start_date).total_seconds() / 3600
        await state.update_data(time_stop= time)
        await state.update_data(stop_dur_date= datetime.now())
        await call.message.edit_text(f"⏸ On pause\n🏄‍♂️ {act}{category}\nMay the focus be with you! 🧘‍♂️", parse_mode=html, reply_markup=nav.stop_menu)
    if call.data== 'rec_resume':
        start_date= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await state.update_data(rec_date=start_date)
        await state.update_data(resume=True)
        await state.update_data(stop_dur_date= None)
        await call.message.edit_text(f"⏳ Recording...\n 🏄‍♂️ {act}{category}\nMay the focus be with you! 🧘‍♂️", reply_markup=nav.record_menu)
    
    
@dp.message_handler(content_types=['text'], state=Focus.Q3)
async def q1_answer(message: types.Message, state: FSMContext):
    if message.text == 'Record activity':
        await state.finish()
        try:
            float(message.text[7:])
            await state.update_data(date=message.text[7:])
        except  Exception as ex:
            pass
            
        messages= ""
        if db.get_count_logs(message.chat.id)[0] == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
        await message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=message.chat.id), parse_mode=html)
        await Focus.Q1.set()
    if message.text == 'Show statistics':
        await state.finish()
        if db.user_info(user_id=message.chat.id) == None:
            db.add_user(user_id=message.chat.id, user_name=message.from_user.username)
        if db.get_user_name(user_id=message.chat.id)[0] == None:
            db.up_name(user_id=message.chat.id, user_name=message.from_user.username)
        actions= []
        _date= date.today()
        view_date= _date.strftime('%a, %d.%m')
        result= db.stat_today(user_id=message.chat.id, date= _date)
        messages=  get_stat_by_action(stat_list=result, actions_list=actions, week=True, user_id=message.chat.id)
        await message.answer(f"🗓 {view_date}{messages}", reply_markup=nav.stat_menu(day='today', split='by actions', list_actions=[]), parse_mode=html)
    else:
        try:
            if message.text.__contains__(':'):
                float(message.text.replace(':', '.'))
                time= message.text.split(':')
                hours= float(int(time[0].strip()) + float(time[1].strip()) / 60)
            elif message.text.__contains__(','):
                hours= float(message.text.replace(',', '.'))
            else:
                hours= float(message.text)
        
        except Exception as ex:
            print(ex)
            await message.answer(f"Your duration is not invalid!\nPlease, type me new duration (example: 1,5 or 1:30)")
            await Focus.Q3.set()
            return
        data = await state.get_data()
        date_log= date.today() if data.get('date') == None else date(year=date.today().year, month=int(data.get('date').split('.')[1]), day= int(data.get('date').split('.')[0]))
        await state.update_data(date=date_log)
        category = '' if data.get('category') == None else data.get('category').split('_')[0]
        act= data.get('action_name')
        if data.get('category') == None:
            multi= 0
            cat= ""
            category=""
        else:
            category= f" /🚦{category} useful"
            multi= int(data.get('category').split('_')[1])
            cat= data.get('category').split('_')[0]
        point= multi * hours
        key= str(uuid.uuid4())
        db.add_focus(user_id=message.chat.id, action=act, hour=hours, date=date_log, category=cat, point=point, key=key)
        view_date= "" if data.get('date') == None else date_log.strftime('%a, %d.%m')
        hours= '&lt;0.1' if hours < 0.1 and hours > 0 else hours#(floor(hours * 10))/10+ int(hours)
        if type(hours) == float:
            if hours == 1.2:
                hours= 1.2
            elif int(hours) >= 1:
                hours= (floor((hours- int(hours)) * 10))/10+ int(hours)
            else:
                hours=(floor(hours * 10))/10+ int(hours)
        elif type(hours) == int:
            hours= int(hours)
        
        count_skip= db.user_info(message.chat.id)[2]
        user_cat=db.get_user_cat(message.chat.id)
        star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
        if (count_skip > 0 and count_skip < 8) and star is True:
            messages=f"{view_date}\n🎉 Added 🕝{hours} / ⭐️0\n🏄‍♂️{act}{category}"
        if count_skip == 0:
            messages=f"{view_date}\n🎉 Added 🕝{hours} / ⭐️{int(point)}\n 🏄‍♂️{act}{category}"
        else:
            messages=f"{view_date}\n🎉 Added 🕝{hours}\n 🏄‍♂️{act}{category}"
        
        if date_log.strftime('%Y.%d.%m') == date.today().strftime('%Y.%d.%m'):
            await message.answer(f"{messages}", reply_markup= nav.focus_menu(key=key), parse_mode=html)
            if db.get_count_logs(user_id=message.chat.id)[0] == 1:
                await message.answer(f"It's your first focus!🔥 Good job!\nUse the buttons below for record activity and show statistics", reply_markup= nav.menu_markup, parse_mode=html)
        else:
            await message.answer(f"{messages}", reply_markup=nav.not_today_menu(data.get('date'), key=key), parse_mode=html)
            if db.get_count_logs(user_id=message.chat.id)[0] == 1:
                await message.answer(f"It's your first focus!🔥 Good job!\nUse the buttons below for record activity and show statistics", reply_markup= nav.menu_markup, parse_mode=html)
        await state.finish()

@dp.callback_query_handler(text_contains= 'foc_') 
@dp.callback_query_handler(text_contains= 'foc_', state=Focus.all_states)
async def answer_message(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    if call.data.__contains__( 'foc_del'):
        key= call.data.split('_')[2]
        log= db.get_stat_by_key(user_id=call.message.chat.id, key=key)
        hour= float(log[2])
        category= log[5]
        act= log[1]
        point= log[3]
        time= '&lt;0.1' if hour < 0.1 and hour > 0 else floor((hour-int(hour)) * 10)/10+ int(hour)
        db.del_focus(user_id=call.message.chat.id, key= key)
        category= f" /🚦{category} useful" if category != "" else ""
        count_skip= db.user_info(call.message.chat.id)[2]
        user_cat=db.get_user_cat(call.message.chat.id)
        star= True if user_cat.__contains__(('Extremely', )) or user_cat.__contains__(('High', )) or user_cat.__contains__(('Medium', )) or user_cat.__contains__(('Low', )) else False
        if (count_skip > 0 and count_skip < 8) and star is True:
            messages=f"🚮 Deleted 🕝{time} / ⭐️0\n🏄‍♂️{act}{category}"
        if count_skip == 0:
            messages=f"🚮 Deleted 🕝{time} / ⭐️{int(point)}\n🏄‍♂️{act}{category}"
        else:
            messages=f"🚮 Deleted 🕝{time}\n🏄‍♂️{act}{category}"
        await call.message.delete()
        await call.message.answer(f"{messages}", reply_markup=nav.add_button, parse_mode=html)
        await state.finish()
    
    if call.data== 'foc_add':
        messages= ""
    
        if db.get_count_logs(user_id=call.message.chat.id)[0] == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
    
        await call.message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=call.message.chat.id), parse_mode=html)
        await state.finish()
        await Focus.Q1.set()

@dp.callback_query_handler(text_contains= 'not_')       
@dp.callback_query_handler(text_contains= 'not_', state=Focus.Q4)
async def answer_message(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)   
    if call.data == 'not_td':
        await state.update_data(date=None)
        messages= ""
    
        if db.get_count_logs(user_id=call.message.chat.id)[0] == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
    
        await call.message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=call.message.chat.id), parse_mode=html)
        await Focus.Q1.set()
    else:
        dt= call.data.split('_')[2]
        await state.update_data(date=dt)
        messages= ""
    
        if db.get_count_logs(user_id=call.message.chat.id)[0] == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
    
        await call.message.answer(f"{messages}", reply_markup=nav.action_menu(user_id=call.message.chat.id), parse_mode=html)
        await Focus.Q1.set()
                    


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
        messages=get_stat_by_action(stat_list=result, actions_list=actions, week=True, user_id=call.message.chat.id)
    elif call.data == 'stat_week_by actions' or call.data == 'stat_week_by day' or call.data == 'stat_month_by week_':
        day='month'
        split= 'by actions'
        first_date= date(year=date.today().year, month=date.today().month, day=1)#.today()- timedelta(days= date.today().weekday())
        days_in_month = calendar.monthrange(year=date.today().year, month=date.today().month)[1]
        second_date= first_date + timedelta(days=days_in_month)
        view_date=f"Month {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
        result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
        messages=get_stat_by_action(stat_list=result, actions_list=actions, user_id=call.message.chat.id)
    elif call.data == 'stat_month_by actions'or call.data == 'stat_month_by week' or call.data == 'stat_all_by week_':
        day='all'
        split= 'by actions'
        if db.first_log(call.message.chat.id)[0] != None:
            old= db.first_log(call.message.chat.id)[0].split('-')
            first_date=  date(year=int(old[0]), month=int(old[1]), day=int(old[2])) 
            second_date= date.today()
            view_date=f"All time {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
            result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=(second_date+timedelta(1)))
            messages=get_stat_by_action(stat_list=result, actions_list=actions, user_id=call.message.chat.id)
        else:
            view_date=f"All time {date.today().strftime('%d.%m')} — {date.today().strftime('%d.%m')}"
            messages= "\nYou haven't been active or you haven't been active this action during this interval of time"
        
    elif call.data == 'stat_all_by actions' or call.data == 'stat_all_by week' or call.data == 'stat_today_by records_':
        day='today'
        split= 'by actions'
        _date= date.today()
        view_date=_date.strftime('%a, %d.%m')
        result= db.stat_today(user_id=call.message.chat.id, date= _date)
        messages=  get_stat_by_action(stat_list=result, actions_list=actions, week=True, user_id=call.message.chat.id)
    
    
    elif call.data == 'stat_today_by actions_':
        day='today'
        split= 'by records'
        _date= date.today()
        view_date=_date.strftime('%a, %d.%m')
        result= db.stat_today(call.message.chat.id, date= _date)
        messages= get_stat_by_records(stat_list=result, actions_list=actions, user_id=call.message.chat.id)
        
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
        if db.first_log(call.message.chat.id)[0] !=None:
            old= db.first_log(call.message.chat.id)[0].split('-')
            old_date= date(year=int(old[0]), month=int(old[1]), day=int(old[2]))
            first_date=  old_date - timedelta(days=old_date.weekday())
            second_date= date.today() + timedelta(days=(7-date.today().weekday()))
            view_date= f"All time {first_date.strftime('%d.%m')} — {(second_date - timedelta(1)).strftime('%d.%m')}"
            messages= get_stat_by_week(user_id=call.message.chat.id, actions_list=actions, first_date=first_date, second_date=second_date)
        else:
            view_date=f"All time {date.today().strftime('%d.%m')} — {date.today().strftime('%d.%m')}"
            messages= "\nYou haven't been active or you haven't been active this action during this interval of time"
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
    if db.get_count_logs(call.message.chat.id)[0] != 0:
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=nav.choose_action_menu(list_actions=actions, user_id=call.message.chat.id))
    else:
        await call.message.edit_text(f"You don't have activity!\nAdd your first focus!", reply_markup=nav.record_button)

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
                messages=  get_stat_by_action(stat_list=result, actions_list=actions_list, week=True, user_id=call.message.chat.id)
            if data.get('day') == 'week':
                first_date= date.today()- timedelta(days= date.today().weekday())
                second_date= first_date + timedelta(weeks=1)
                view_date=f"Week {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
                result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
                messages=get_stat_by_action(stat_list=result, actions_list=actions_list, week=True, user_id=call.message.chat.id)
            if data.get('day') == 'month':
                first_date= date(year=date.today().year, month=date.today().month, day=1)#.today()- timedelta(days= date.today().weekday())
                days_in_month = calendar.monthrange(year=date.today().year, month=date.today().month)[1]
                second_date= first_date + timedelta(days=days_in_month)
                view_date=f"Month {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
                result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
                messages=get_stat_by_action(stat_list=result, actions_list=actions_list, user_id=call.message.chat.id)
            if data.get('day') == 'all':
                old= db.first_log(call.message.chat.id)[0].split('-')
                first_date=  date(year=int(old[0]), month=int(old[1]), day=int(old[2])) 
                second_date= date.today()
                view_date=f"All time {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
                result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
                messages=get_stat_by_action(stat_list=result, actions_list=actions_list, user_id=call.message.chat.id)
        else:
            if data.get('day') == 'today':
                _date= date.today()
                view_date=_date.strftime('%a, %d.%m')
                result= db.stat_today(call.message.chat.id, date= _date)
                messages= get_stat_by_records(stat_list=result, actions_list=actions_list, user_id=call.message.chat.id)
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
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=nav.choose_action_menu(list_actions=[], user_id=call.message.chat.id))
    elif call.data.split('_')[1] == 'ex':
        action= call.data.split('_')[2]
        actions_list.remove(action)
        await state.update_data(actions=actions_list)
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=nav.choose_action_menu(list_actions=actions_list, user_id=call.message.chat.id))
    else:
        action= call.data.split('_')[1]
        actions_list.append(action)
        await state.update_data(actions=actions_list)
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=nav.choose_action_menu(list_actions=actions_list, user_id=call.message.chat.id))
              
#Notification
async def every_mon():
    for user_id in db.user_info_id():
        try:
            await dp.bot.send_message(chat_id=user_id, text=f"🎉 It was a great week!\nYou got ⭐️ <b>{int(db.get_points_atweek(user_id)[0])}</b> for this 7 days", parse_mode=html)
        except:
            pass
        
async def every_day():
    for user_id in db.user_info_id():
        if db.stat_today(user_id=user_id, date=date.today()) != None:
            if int(db.get_user_shoke(user_id)[0]) != 0:
                try:
                    await dp.bot.send_message(chat_id=user_id, text=f"🤜🤛 Just do it! You have shock mode 🔥{int(db.get_user_shoke(user_id)[0])} days. Don't lose it!", parse_mode=html, reply_markup=nav.log_button)
                except:
                    pass
        else:
            if int(db.get_user_shoke(user_id)[0]) != 0: 
                try:
                    await dp.bot.send_message(chat_id=user_id, text=f"🤜🤛 Just do it! You have shock mode 🔥{int(db.get_user_shoke(user_id)[0])} days. Don't lose it!", parse_mode=html, reply_markup=nav.log_button)
                except:
                    pass
                
async def check_shoke():
    for user_id in db.user_info_id():
        if len(db.stat_today(user_id=user_id, date=date.today()- timedelta(1))) != 0:
            db.shoke_user(user_id=user_id)
        else:
            db.shoke_user(user_id=user_id, sk=False)

async def scheduler():
    aioschedule.every().monday.at("10:00").do(every_mon)
    aioschedule.every().day.at("11:00").do(check_shoke)
    #aioschedule.every().minute.do(every_mon)
    aioschedule.every().day.at("12:00").do(every_day)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Restart bot'),
            types.BotCommand('stat', 'Your stats'),
            types.BotCommand('focus', 'Log activity'),
            types.BotCommand('friend', 'Your friends'),
        ]
    )

async def notification(_):
    await set_default_commands(dp)
    asyncio.create_task(scheduler())
    




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=notification)