from subprocess import call
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from db import Databae

db= Databae('database.db')

main_menu= InlineKeyboardMarkup(row_width=1)

analyse= InlineKeyboardButton('Analyse what your time is spent on', callback_data='start')
increase= InlineKeyboardButton('Increase time for useful activities', callback_data='start')
become= InlineKeyboardButton('Become more productive', callback_data='start')
other= InlineKeyboardButton('Other', callback_data='start')

main_menu.add(analyse, increase, become, other)

record_button = InlineKeyboardMarkup(row_width=1)
record= InlineKeyboardButton('Record activity', callback_data='record')

record_button.add(record)

log_menu = InlineKeyboardMarkup(row_width=1)
start= InlineKeyboardButton('Start recording', callback_data='log_start')
enter= InlineKeyboardButton('Enter duration', callback_data='log_enter')

log_menu.add(start, enter)

focus_menu = InlineKeyboardMarkup(row_width=1)
delete= InlineKeyboardButton('Delete entry 🚮', callback_data='foc_del')
add= InlineKeyboardButton('Add one more Focus', callback_data='foc_add')

focus_menu.add(delete, add)

add_button = InlineKeyboardMarkup(row_width=1)
add_= InlineKeyboardButton('Add Focus', callback_data='foc_add')

add_button.add(add_)

log_button = InlineKeyboardMarkup(row_width=1)
log_= InlineKeyboardButton('Log action', callback_data='foc_add')

log_button.add(log_)

add_friends_button = InlineKeyboardMarkup(row_width=1)
friend= InlineKeyboardButton('Add friend', callback_data='friend_add')

add_friends_button.add(friend)


friends_menu = InlineKeyboardMarkup(row_width=1)
show= InlineKeyboardButton('Show stats of my friends', callback_data='friend_show')
add_friend= InlineKeyboardButton('Add one more friend', callback_data='friend_add')

friends_menu.add(add_friend, show)

add_friends_menu = InlineKeyboardMarkup(row_width=1)
reject= InlineKeyboardButton('❌ Reject', callback_data='Reject')
add_friend_true= InlineKeyboardButton('Add one more friend', callback_data='to_add')

add_friends_menu.add(add_friend_true, reject)

def not_today_menu(date):
    not_today = InlineKeyboardMarkup(row_width=1)
    delete= InlineKeyboardButton('Delete entry 🚮', callback_data='foc_del')
    add= InlineKeyboardButton(f'Add one more Focus [{date}]', callback_data='tod_add_' + str(date))
    add_today= InlineKeyboardButton('Add one more Focus [today]', callback_data='tod_today')

    return not_today.add(delete, add, add_today)
    

def stat_menu(day, split, list_actions):
    stat= InlineKeyboardMarkup(row_width=1)
    
    period= InlineKeyboardButton(f'Period: {day} →', callback_data='stat_'+ str(day)+ f'_{split}')
    spliting= InlineKeyboardButton(f'Spliting: {split} →', callback_data='stat_'+ str(day)+ f'_{split}_')
    if len(list_actions) != 0:
        activity= InlineKeyboardButton('Activity: you choose', callback_data='act_'+ str(day)+ f'_{split}')
    else:
        activity= InlineKeyboardButton('Activity: all', callback_data='act_'+ str(day)+ f'_{split}') 
    

    return stat.add(period, spliting, activity)

def choose_action_menu(list_actions, user_id):
    choose_action = InlineKeyboardMarkup(row_width=2)
    
    done= InlineKeyboardButton('Done', callback_data='choose_done')
    reset= InlineKeyboardButton('Reset', callback_data='choose_reset')
    actions= []
    for name in db.inf_about_action(user_id=user_id):
        actions.append(name[0])
    actions.sort(key=str.__len__)
    for action in actions:
        if list(list_actions).__contains__(action):
            act = InlineKeyboardButton(f'{action} ✔', callback_data='choose_'+str(action))
        else:
            act = InlineKeyboardButton(f'{action}', callback_data='choose_'+str(action))
        if len(action) >= 20:
            choose_action.add(act)
        else:
            choose_action.insert(act)
    
    return choose_action.add(reset, done)
    
def action_menu(user_id):
    actions_menu= InlineKeyboardMarkup(row_width=2)
    
    actions= db.last_actions(user_id=user_id)
    for action in actions:
        name= InlineKeyboardButton(f'{action[0]}', callback_data='act_'+str(action[0])) 
        if len(action[0]) >= 20:
            actions_menu.add(name)
        else:
            actions_menu.insert(name)
            
    return actions_menu

def categories_menu():
    keyboard= InlineKeyboardMarkup(row_width=2)
    
    low= InlineKeyboardButton(f'Low ⭐️1', callback_data='cat_Low_1')
    medium= InlineKeyboardButton(f'Medium ⭐️2', callback_data='cat_Medium_2')
    high= InlineKeyboardButton(f'High ⭐️3', callback_data='cat_High_3')
    extremely= InlineKeyboardButton(f'Extremely ⭐️4', callback_data='cat_Extremely_4')
    skip= InlineKeyboardButton(f'Skip', callback_data='cat_Skip')

    return keyboard.add(low, medium, high, extremely, skip)
    
