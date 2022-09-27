from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from db import Database

db= Database('database.db')

main_menu= InlineKeyboardMarkup(row_width=1)

analyse= InlineKeyboardButton('Analyse what your time is spent on', callback_data='start')
increase= InlineKeyboardButton('Increase time for useful activities', callback_data='start')
become= InlineKeyboardButton('Become more productive', callback_data='start')
other= InlineKeyboardButton('Other', callback_data='start')

main_menu.add(analyse, increase, become, other)

menu_markup= ReplyKeyboardMarkup(resize_keyboard=True )

menu_markup.add('Record activity', 'Show statistics')

record_button = InlineKeyboardMarkup(row_width=1)
record= InlineKeyboardButton('Record activity', callback_data='record')

record_button.add(record)

record_menu = InlineKeyboardMarkup(row_width=1)
pause= InlineKeyboardButton('Pause', callback_data='rec_pause')
stop= InlineKeyboardButton('Stop', callback_data='rec_stop')

record_menu.add(pause, stop)

stop_menu = InlineKeyboardMarkup(row_width=1)
resume= InlineKeyboardButton('Resume', callback_data='rec_resume')
stop= InlineKeyboardButton('Stop', callback_data='rec_stop')

stop_menu.add(resume, stop)

log_menu = InlineKeyboardMarkup(row_width=1)
start= InlineKeyboardButton('Start recording', callback_data='log_start')
enter= InlineKeyboardButton('Enter duration', callback_data='log_enter')

log_menu.add(start, enter)

def focus_menu(key):
    focus_menu = InlineKeyboardMarkup(row_width=1)
    delete= InlineKeyboardButton('Delete entry 🚮', callback_data='foc_del_'+ str(key))
    add= InlineKeyboardButton('Add one more Focus', callback_data='foc_add')

    return focus_menu.add(delete, add)

add_button = InlineKeyboardMarkup(row_width=1)
add_= InlineKeyboardButton('Add Focus', callback_data='foc_add')

add_button.add(add_)

log_button = InlineKeyboardMarkup(row_width=1)
log_= InlineKeyboardButton('Log action', callback_data='foc_add')

log_button.add(log_)

add_friends_button = InlineKeyboardMarkup(row_width=1)
friend= InlineKeyboardButton('Add friend', callback_data='friend')

add_friends_button.add(friend)

def rej_markup(user_name):
    change_rej_button = InlineKeyboardMarkup(row_width=1)
    change_rej= InlineKeyboardButton('Changed my mind, reject', callback_data='change_rej%'+str(user_name))

    return change_rej_button.add(change_rej)

def add_markup(user_name):
    change_add_button = InlineKeyboardMarkup(row_width=1)
    change_add= InlineKeyboardButton('Changed my mind, add to friends', callback_data='change_add%'+str(user_name))

    return change_add_button.add(change_add)

friends_menu = InlineKeyboardMarkup(row_width=1)
show= InlineKeyboardButton('Show stats of my friends', callback_data='friend_show')
add_friend= InlineKeyboardButton('Add one more friend', callback_data='friend_add')

friends_menu.add(add_friend, show)

show_friend_button= InlineKeyboardMarkup(row_width=1)
show_friend_button.add(show)

def next_menu(i, user_id):
    j= len(db.get_friends(user_id)[0].split(','))-1
    next_markup= InlineKeyboardMarkup(row_width=1)
    next= InlineKeyboardButton(f'Friend {i+1}/{j} >', callback_data='next_'+str(i))
    add_friend= InlineKeyboardButton('Add friend', callback_data='friend_add')
    return next_markup.add(next, add_friend)

def add_friends_menu(user_name):
    add_friends = InlineKeyboardMarkup(row_width=1)
    reject= InlineKeyboardButton('❌ Reject', callback_data='to_rej%'+str(user_name))
    add_friend_true= InlineKeyboardButton('Add to friends', callback_data='to_add%'+str(user_name))

    return add_friends.add(add_friend_true, reject)

def not_today_menu(date, key):
    not_today = InlineKeyboardMarkup(row_width=1)
    delete= InlineKeyboardButton('Delete entry 🚮', callback_data='foc_del_'+ str(key))
    add= InlineKeyboardButton(f'Add one more Focus [{date}]', callback_data='not_dd_' + str(date))
    add_today= InlineKeyboardButton('Add one more Focus [today]', callback_data='not_td')

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
    for name in db.last_actions(user_id=user_id):
        actions.append(name[0])
    actions.sort(key=str.__len__)
    for action in actions:
        if list(list_actions).__contains__(action):
            act = InlineKeyboardButton(f'{action} ✔', callback_data='choose_ex_'+str(action))
        else:
            act = InlineKeyboardButton(f'{action}', callback_data='choose_'+str(action))
        if len(action) >= 20:
            choose_action.add(act)
        else:
            choose_action.insert(act)
    
    return choose_action.add(reset, done)
    
def action_menu(user_id):
    actions_menu= InlineKeyboardMarkup(row_width=2)
    
    actions= reversed(db.last_actions(user_id=user_id))
    print(db.last_actions(user_id=user_id))
    i=0
    for action in actions:
        if i == 10:
            break
        name= InlineKeyboardButton(f'{action[0]}', callback_data='act_'+str(action[0])) 
        if len(action[0]) >= 20:
            actions_menu.add(name)
        else:
            actions_menu.insert(name)
        i+=1
            
    return actions_menu

def categories_menu():
    keyboard= InlineKeyboardMarkup(row_width=2)
    
    low= InlineKeyboardButton(f'Low ⭐️1', callback_data='cat_Low_1')
    medium= InlineKeyboardButton(f'Medium ⭐️2', callback_data='cat_Medium_2')
    high= InlineKeyboardButton(f'High ⭐️3', callback_data='cat_High_3')
    extremely= InlineKeyboardButton(f'Extremely ⭐️4', callback_data='cat_Extremely_4')
    skip= InlineKeyboardButton(f'Skip', callback_data='cat_Skip')

    return keyboard.add(low, medium, high, extremely, skip)
    
