from loader import db, dp, html
from aiogram.dispatcher import FSMContext
from src.keyboards.inline.stats import stat_menu, choose_action_menu
from src.keyboards.inline.focus import record_button
from aiogram.types import Message, CallbackQuery
from src.handlers import other
from datetime import datetime, date, timedelta
import calendar



@dp.callback_query_handler(text_contains= 'act_')
async def act_message(call: CallbackQuery, state: FSMContext):
    response=call.data.split('_')
    data= await state.get_data()
    list_actions= data.get('actions') if data.get('actions') else []
    await state.update_data(day=response[1])
    await state.update_data(split=response[2])
    if db.count_logs(call.message.chat.id) != 0:
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=choose_action_menu(list_actions=list_actions, user_id=call.message.chat.id))

@dp.callback_query_handler(text_contains= 'choose_')
async def choose_message(call: CallbackQuery, state: FSMContext):
    response= call.data.split('_')
    data= await state.get_data()
    list_actions= data.get('actions') if data.get('actions') else []
    if response[1] == 'done':
        day= data.get('day')
        split= data.get('split')
        message= other.stat_message(
            user_id=call.message.chat.id,
            action_list=list_actions,
            period=day,
            split=split
        )
        await call.message.edit_text(f"{message}", reply_markup=stat_menu(period=day, split=split, list_actions=list_actions),
                     parse_mode=html)
    elif response[1] == 'reset':
        await state.update_data(actions=[])
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=choose_action_menu(list_actions=[], user_id=call.message.chat.id))
    elif response[1] == 'ch':
        list_actions.remove(response[2])
        await state.update_data(actions=list_actions)
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=choose_action_menu(list_actions=list_actions, user_id=call.message.chat.id))
    elif response[1] == 'nch':
        list_actions.append(response[2])
        await state.update_data(actions=list_actions)
        await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=choose_action_menu(list_actions=list_actions, user_id=call.message.chat.id))

@dp.callback_query_handler(text_contains= 'per_')
async def per_message(call: CallbackQuery, state: FSMContext):
    response= call.data.split('_')
    data= await state.get_data()    
    list_actions= data.get('actions') if data.get('actions') else []
    if response[1] == 'today':
        period='week'
    elif response[1] == 'week':
        period= 'month'
    elif response[1] == 'month':
        period= 'all'
    else:
        period='today'
    message= other.stat_message(
            user_id=call.message.chat.id,
            action_list=list_actions,
            period=period,
            split='by actions' 
    )
    await call.message.edit_text(f"{message}", reply_markup=stat_menu(period=period, split='by actions', list_actions=list_actions),
                     parse_mode=html)

@dp.callback_query_handler(text_contains= 'split_')
async def stat_message(call: CallbackQuery, state: FSMContext):
    response= call.data.split('_')
    data= await state.get_data()    
    list_actions= data.get('actions') if data.get('actions') else []
    if response[1] == 'today':
        if response[2] == 'by actions':
           split= 'by records' 
        else:
            split= 'by actions'
    elif response[1] == 'week':
        if response[2] == 'by actions':
            split= 'by day' 
        else:
            split= 'by actions'
    elif response[1] == 'month':
        if response[2] == 'by actions':
               split= 'by week' 
        else:
            split= 'by actions'
    else:
        if response[2] == 'by actions':
           split= 'by week'
        else:
            split= 'by actions'
    message= other.stat_message(
            user_id=call.message.chat.id,
            action_list=list_actions,
            period=response[1],
            split=split
    )
    await call.message.edit_text(f"{message}", reply_markup=stat_menu(period=response[1], split=split, list_actions=list_actions),
                     parse_mode=html)

# @dp.callback_query_handler(text_contains= 'stat_')
# async def stat_message(call: CallbackQuery, state: FSMContext):
#     data= await state.get_data()
#     actions= data.get('actions')
#     print(actions)
#     day=''
#     split=''
#     if actions == None: 
#         actions= []
#     if call.data == 'stat_today_by actions' or call.data == 'stat_today_by records' or call.data == 'stat_week_by day_':
#         day='week'
#         split= 'by actions'
#         first_date= date.today()- timedelta(days= date.today().weekday())
#         second_date= first_date + timedelta(weeks=1)
#         view_date=f"Week {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
#         result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
#         messages=other.get_stat_by_action(stat_list=result, actions_list=actions, week=True, user_id=call.message.chat.id)
#     elif call.data == 'stat_week_by actions' or call.data == 'stat_week_by day' or call.data == 'stat_month_by week_':
#         day='month'
#         split= 'by actions'
#         first_date= date(year=date.today().year, month=date.today().month, day=1)#.today()- timedelta(days= date.today().weekday())
#         days_in_month = calendar.monthrange(year=date.today().year, month=date.today().month)[1]
#         second_date= first_date + timedelta(days=days_in_month)
#         view_date=f"Month {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
#         result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
#         messages=other.get_stat_by_action(stat_list=result, actions_list=actions, user_id=call.message.chat.id)
#     elif call.data == 'stat_month_by actions'or call.data == 'stat_month_by week' or call.data == 'stat_all_by week_':
#         day='all'
#         split= 'by actions'
#         if db.first_log(call.message.chat.id)[0] != None:
#             old= db.first_log(call.message.chat.id)[0].split('-')
#             first_date=  date(year=int(old[0]), month=int(old[1]), day=int(old[2])) 
#             second_date= date.today()
#             view_date=f"All time {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
#             result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=(second_date+timedelta(1)))
#             messages=other.get_stat_by_action(stat_list=result, actions_list=actions, user_id=call.message.chat.id)
#         else:
#             view_date=f"All time {date.today().strftime('%d.%m')} — {date.today().strftime('%d.%m')}"
#             messages= "\nYou haven't been active or you haven't been active this action during this interval of time"
        
#     elif call.data == 'stat_all_by actions' or call.data == 'stat_all_by week' or call.data == 'stat_today_by records_':
#         day='today'
#         split= 'by actions'
#         _date= date.today()
#         view_date=_date.strftime('%a, %d.%m')
#         result= db.stat_today(user_id=call.message.chat.id, date= _date)
#         messages=  other.get_stat_by_action(stat_list=result, actions_list=actions, week=True, user_id=call.message.chat.id)
    
    
#     elif call.data == 'stat_today_by actions_':
#         day='today'
#         split= 'by records'
#         _date= date.today()
#         view_date=_date.strftime('%a, %d.%m')
#         result= db.stat_today(call.message.chat.id, date= _date)
#         messages= other.get_stat_by_records(stat_list=result, actions_list=actions, user_id=call.message.chat.id)
        
#     elif call.data == 'stat_week_by actions_':
#         day='week'
#         split= 'by day'
#         first_date= date.today() - timedelta(7)
#         second_date= date.today() + timedelta(1)
#         view_date= f"Week {first_date.strftime('%d.%m')} — {date.today().strftime('%d.%m')}"
#         messages=other.get_stat_by_day(call.message.chat.id, actions, first_date, second_date)
#     elif call.data == 'stat_month_by actions_':
#         day='month'
#         split= 'by week'
#         first_date= date.today()- timedelta(days= date.today().weekday()) - timedelta(weeks=4)
#         second_date= date.today() + timedelta(days=(6-date.today().weekday()))
#         view_date= f"Month {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
#         messages= other.get_stat_by_week(user_id=call.message.chat.id, actions_list=actions, first_date=first_date, second_date=second_date)
#     elif call.data == 'stat_all_by actions_':
#         day='all'
#         split= 'by week'
#         if db.first_log(call.message.chat.id)[0] !=None:
#             old= db.first_log(call.message.chat.id)[0].split('-')
#             old_date= date(year=int(old[0]), month=int(old[1]), day=int(old[2]))
#             first_date=  old_date - timedelta(days=old_date.weekday()) 
#             second_date= date.today() + timedelta(days=(7-date.today().weekday()))
#             view_date= f"All time {first_date.strftime('%d.%m')} — {(second_date - timedelta(1)).strftime('%d.%m')}"
#             messages= other.get_stat_by_week(user_id=call.message.chat.id, actions_list=actions, first_date=first_date, second_date=second_date)
#         else:
#             view_date=f"All time {date.today().strftime('%d.%m')} — {date.today().strftime('%d.%m')}"
#             messages= "\nYou haven't been active or you haven't been active this action during this interval of time"
#     await call.message.edit_text(text=f"🗓 {view_date}{messages}", reply_markup=stat_menu(day=day, split=split, list_actions=actions), parse_mode=html)
    
# @dp.callback_query_handler(text_contains= 'act_')
# async def act_message(call: CallbackQuery, state: FSMContext):
#     data= await state.get_data()
#     actions= data.get('actions')
#     if actions == None:
#         actions= []
#     day_=call.data.split('_')[1]
#     split_= call.data.split('_')[2]
#     await state.update_data(day=day_)
#     await state.update_data(split=split_)
#     if db.count_logs(call.message.chat.id) != 0:
#         await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=stats.choose_action_menu(list_actions=actions, user_id=call.message.chat.id))
#     else:
#         await call.message.edit_text(f"You don't have activity!\nAdd your first focus!", reply_markup=record_button)

# @dp.callback_query_handler(text_contains= 'choose_')
# async def choose_message(call: CallbackQuery, state: FSMContext):
#     data= await state.get_data()
#     print(call.data)
#     actions_list= []
#     if data.get('actions') != None:
#         for act in data.get('actions'):
#             actions_list.append(act)
#     if call.data == 'choose_done':
#         if data.get('split') == 'by actions':
#             if data.get('day') == 'today':
#                 _date= date.today()
#                 view_date= _date.strftime("%d.%m")
#                 result= db.stat_today(user_id=call.message.chat.id, date= _date)
#                 messages=  other.get_stat_by_action(stat_list=result, actions_list=actions_list, week=True, user_id=call.message.chat.id)
#             if data.get('day') == 'week':
#                 first_date= date.today()- timedelta(days= date.today().weekday())
#                 second_date= first_date + timedelta(weeks=1)
#                 view_date=f"Week {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
#                 result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
#                 messages=other.get_stat_by_action(stat_list=result, actions_list=actions_list, week=True, user_id=call.message.chat.id)
#             if data.get('day') == 'month':
#                 first_date= date(year=date.today().year, month=date.today().month, day=1)#.today()- timedelta(days= date.today().weekday())
#                 days_in_month = calendar.monthrange(year=date.today().year, month=date.today().month)[1]
#                 second_date= first_date + timedelta(days=days_in_month)
#                 view_date=f"Month {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}"
#                 result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
#                 messages=other.get_stat_by_action(stat_list=result, actions_list=actions_list, user_id=call.message.chat.id)
#             if data.get('day') == 'all':
#                 old= db.first_log(call.message.chat.id)[0].split('-')
#                 first_date=  date(year=int(old[0]), month=int(old[1]), day=int(old[2])) 
#                 second_date= date.today()
#                 view_date=f"All time {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
#                 result= db.stat_by_interval(user_id=call.message.chat.id, first_date=first_date, second_date=second_date)
#                 messages=other.get_stat_by_action(stat_list=result, actions_list=actions_list, user_id=call.message.chat.id)
#         else:
#             if data.get('day') == 'today':
#                 _date= date.today()
#                 view_date=_date.strftime('%a, %d.%m')
#                 result= db.stat_today(call.message.chat.id, date= _date)
#                 messages= other.get_stat_by_records(stat_list=result, actions_list=actions_list, user_id=call.message.chat.id)
#             if data.get('day') == 'week':
#                 first_date= date.today() - timedelta(weeks=1)
#                 second_date= date.today()
#                 view_date= f"{first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
                
#             if data.get('day') == 'month':
#                 first_date= date.today()- timedelta(days= date.today().weekday()) - timedelta(weeks=4)
#                 second_date= date.today() + timedelta(days=(6-date.today().weekday()))
#                 view_date= f"Month {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}"
#                 messages= other.get_stat_by_week(user_id=call.message.chat.id, actions_list=actions_list, first_date=first_date, second_date=second_date)
#             if data.get('day') == 'all':
#                 old= db.first_log(call.message.chat.id)[0].split('-')
#                 old_date= date(year=int(old[0]), month=int(old[1]), day=int(old[2]))
#                 first_date=  old_date - timedelta(days=old_date.weekday())
#                 second_date= date.today() + timedelta(days=(7-date.today().weekday()))
#                 view_date= f"Week {first_date.strftime('%d.%m')} — {(second_date - timedelta(1)).strftime('%d.%m')}"
#                 messages= other.get_stat_by_week(user_id=call.message.chat.id, actions_list=actions_list, first_date=first_date, second_date=second_date)
#         await call.message.edit_text(f"🗓 {view_date}{messages}", reply_markup=stats.stat_menu(day=data.get('day'), split=data.get('split'), list_actions=actions_list), parse_mode=html)
    
#     elif call.data == 'choose_reset':
#         actions_list.clear()
#         await state.update_data(actions=actions_list)
#         await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=stats.choose_action_menu(list_actions=[], user_id=call.message.chat.id))
#     elif call.data.split('_')[1] == 'ex':
#         action= call.data.split('_')[2]
#         actions_list.remove(action)
#         await state.update_data(actions=actions_list)
#         await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=stats.choose_action_menu(list_actions=actions_list, user_id=call.message.chat.id))
#     else:
#         action= call.data.split('_')[1]
#         actions_list.append(action)
#         await state.update_data(actions=actions_list)
#         await call.message.edit_text(f"Select  activity 🏄‍♂️", reply_markup=stats.choose_action_menu(list_actions=actions_list, user_id=call.message.chat.id))
        
