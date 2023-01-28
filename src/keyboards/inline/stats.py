from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from loader import db

def choose_action_menu(list_actions: list, user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    actions= db.last_actions(user_id=user_id)
    for action in actions:
        if action[0]:
            if list_actions.__contains__(str(action[0])):
                act = InlineKeyboardButton(f'{action[0]} ✔', callback_data='choose_ch_'+str(action[0]))
            else:
                act = InlineKeyboardButton(f'{action[0]}', callback_data='choose_nch_'+str(action[0]))
            if len(str(action[0])) >= 20:
                markup.add(act)
            else:
                markup.insert(act)
    
    markup.add(
        InlineKeyboardButton('Done', callback_data='choose_done'),
        InlineKeyboardButton('Reset', callback_data='choose_reset')
    )
    
    return markup

def stat_menu(period, split, list_actions):
    markup= InlineKeyboardMarkup(row_width=1)
    
    markup.add(
        InlineKeyboardButton(f'Period: {period} →', callback_data=f'per_{period}_{split}'),
        InlineKeyboardButton(f'Spliting: {split} →', callback_data=f'split_{period}_{split}')
    )
    if len(list_actions) != 0:
        choose= ', '.join(list_actions)
        activity= InlineKeyboardButton(f'Activity: {choose}', callback_data=f'act_{period}_{split}')
    else:
        activity= InlineKeyboardButton('Activity: all', callback_data=f'act_{period}_{split}') 
    
    markup.add(
        activity
    )

    return markup