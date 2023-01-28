from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from loader import db

record_button = InlineKeyboardMarkup(row_width=1)

record_button.add(
    InlineKeyboardButton('Record activity', callback_data='record')
    )

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

def action_menu(user_id):
    actions_menu= InlineKeyboardMarkup(row_width=2)
    
    actions= db.last_actions(user_id=user_id)
    print(db.last_actions(user_id=user_id))
    for action in actions:
        if action[0]:
            name= InlineKeyboardButton(f'{action[0]}', callback_data='act_'+str(action[0])) 
            if len(str(action[0])) >= 20:
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

def not_today_menu(date, key):
    not_today = InlineKeyboardMarkup(row_width=1)
    delete= InlineKeyboardButton('Delete entry 🚮', callback_data='foc_del_'+ str(key))
    add= InlineKeyboardButton(f'Add one more Focus [{date}]', callback_data='not_dd_' + str(date))
    add_today= InlineKeyboardButton('Add one more Focus [today]', callback_data='not_td')

    return not_today.add(delete, add, add_today)

add_button = InlineKeyboardMarkup(row_width=1)
add_= InlineKeyboardButton('Add Focus', callback_data='foc_add')
add_button.add(add_)

log_button = InlineKeyboardMarkup(row_width=1)
log_= InlineKeyboardButton('Log action', callback_data='foc_add')
log_button.add(log_)