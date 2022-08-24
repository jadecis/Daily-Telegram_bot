from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

main_menu= InlineKeyboardMarkup(row_width=1)

analyse= InlineKeyboardButton('Analyse what your time is spent on', callback_data='analyse')
increase= InlineKeyboardButton('Increase time for useful activities', callback_data='increase')
become= InlineKeyboardButton('Become more productive', callback_data='become')
other= InlineKeyboardButton('Other', callback_data='other')

main_menu.add(analyse, increase, become, other)