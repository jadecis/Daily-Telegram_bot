from subprocess import call
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

main_menu= InlineKeyboardMarkup(row_width=1)

analyse= InlineKeyboardButton('Analyse what your time is spent on', callback_data='start')
increase= InlineKeyboardButton('Increase time for useful activities', callback_data='start')
become= InlineKeyboardButton('Become more productive', callback_data='start')
other= InlineKeyboardButton('Other', callback_data='start')

main_menu.add(analyse, increase, become, other)

record_button = InlineKeyboardMarkup(row_width=1)
record= InlineKeyboardButton('Record activity', callback_data='record')

record_button.add(record)

def stat_menu(day, split, list_actions):
    stat= InlineKeyboardMarkup(row_width=1)
    
    period= InlineKeyboardButton(f'Period: {day} →', callback_data='stat_'+ str(day)+ f'_{split}')
    spliting= InlineKeyboardButton(f'Spliting: {split} →', callback_data='stat_'+ str(day)+ f'_{split}_')
    if len(list_actions) != 0:
        activity= InlineKeyboardButton('Activity: you choose', callback_data='act_'+ str(day)+ f'_{split}')
    else:
        activity= InlineKeyboardButton('Activity: all', callback_data='act_'+ str(day)+ f'_{split}') 
    

    return stat.add(period, spliting, activity)

def choose_action_menu(list_actions):
    choose_action = InlineKeyboardMarkup(row_width=2)
    
    done= InlineKeyboardButton('Done', callback_data='choose_done')
    reset= InlineKeyboardButton('Reset', callback_data='choose_reset')
    actions= ['Work', 'second', 'third', 'fourthwert1234567890', 'fiveth']
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
    
