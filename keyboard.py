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

def stat_menu(day, split):
    stat= InlineKeyboardMarkup(row_width=1)
    
    period= InlineKeyboardButton(f'Period: {day} →', callback_data='stat_'+ str(day)+ f'_{split}')
    spliting= InlineKeyboardButton(f'Spliting: {split} →', callback_data='stat_'+ str(day)+ f'_{split}_')
    activity= InlineKeyboardButton('Activity: all', callback_data='stat_all') 
    

    return stat.add(period, spliting, activity)

def choose_action_menu(list_actions):
    choose_action = InlineKeyboardMarkup(row_width=2)
    
    done= InlineKeyboardButton('Done', callback_data='choose_done')
    reset= InlineKeyboardButton('Reset', callback_data='choose_reset')
    actions= ['first', 'second', 'third', 'fourth']
    for action in actions:
        if list(list_actions).__contains__(action):
            act = InlineKeyboardButton(f'{action} ☑️', callback_data='choose_'+str(action))
        else:
            act = InlineKeyboardButton(f'{action}', callback_data='choose_'+str(action))
        choose_action.insert(act)
    
    return choose_action.add(reset, done)
    
