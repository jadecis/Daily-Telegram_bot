from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from loader import db

main_menu= InlineKeyboardMarkup(row_width=1)

analyse= InlineKeyboardButton('Analyse what your time is spent on', callback_data='start')
increase= InlineKeyboardButton('Increase time for useful activities', callback_data='start')
become= InlineKeyboardButton('Become more productive', callback_data='start')
other= InlineKeyboardButton('Other', callback_data='start')
main_menu.add(analyse, increase, become, other)

add_friend_button = InlineKeyboardMarkup(row_width=1)
add_friend_button.add(
                       InlineKeyboardButton('Add friend', callback_data='friend')
                       )

def rej_markup(user_name):
    change_rej_button = InlineKeyboardMarkup(row_width=1)
    change_rej= InlineKeyboardButton('Changed my mind, reject', callback_data='change_rej_'+str(user_name))

    return change_rej_button.add(change_rej)

def add_markup(user_name):
    change_add_button = InlineKeyboardMarkup(row_width=1)
    change_add= InlineKeyboardButton('Changed my mind, add to friends', callback_data='change_add_'+str(user_name))

    return change_add_button.add(change_add)

friends_menu = InlineKeyboardMarkup(row_width=1)

friends_menu.add(
    InlineKeyboardButton('Show stats of my friends', callback_data='friend_show'),
    InlineKeyboardButton('Add one more friend', callback_data='friend_add')
)

show_friend_button= InlineKeyboardMarkup(row_width=1)
show_friend_button.add(
    InlineKeyboardButton('Show stats of my friends', callback_data='show')
)

def next_menu(i, user_id):
    j= len(db.get_friends(user_id))
    next_markup= InlineKeyboardMarkup(row_width=1)
    next= InlineKeyboardButton(f'Friend {i+1}/{j} >', callback_data='next_'+str(i))
    add_friend= InlineKeyboardButton('Add friend', callback_data='friend_add')
    return next_markup.add(next, add_friend)

def add_friends_menu(user_name):
    markup = InlineKeyboardMarkup(row_width=1)
    
    markup.add(
            InlineKeyboardButton('❌ Reject', callback_data='submit_rej_'+str(user_name)),
            InlineKeyboardButton('✅ Add to friends', callback_data='submit_add_'+str(user_name))
    )
    return markup