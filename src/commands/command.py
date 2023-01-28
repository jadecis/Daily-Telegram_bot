from loader import Focus, html, dp, db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery
from src.keyboards.inline.other import main_menu 
from src.keyboards.inline.focus import record_button, action_menu
from src.keyboards.inline.stats import stat_menu
from src.keyboards.inline.other import add_friend_button, next_menu
from src.keyboards.reply.main_button import menu_markup
from datetime import date, datetime
from src.handlers import other

@dp.message_handler(CommandStart(), state="*")
@dp.message_handler(CommandStart())
async def start_message(msg: Message, state: FSMContext):
    await state.finish()
    res= db.user_info(msg.chat.id)
    if not(res):
        db.add_user(
            msg.chat.id,
            msg.chat.username
        )
    else:
        if res[2] == None:
            db.up_name(
                msg.chat.id,
                msg.chat.username
            )
    await msg.answer(f"Hello! This is a bot for tracking your daily activities. What is your goal?", reply_markup=main_menu)
    
@dp.callback_query_handler(text= 'start')
async def answer_message(call: CallbackQuery):
    await call.message.answer(f"Great! This bot helps you to record how much time you spent on various activities."
                              +f"The bot will store and show you how productive you were in different days, weeks and months.\n\nNow let's record your first activity!",
                                reply_markup= record_button)

@dp.message_handler(commands=['s'], state="*")
@dp.message_handler(commands=['s'])
async def markup_handler(msg: Message):
    await msg.answer("New keyboard", reply_markup=menu_markup)


@dp.message_handler(commands=['stat'], state="*")
@dp.message_handler(commands=['stat'])
async def com_stat_message(msg: Message, state: FSMContext):
    await state.finish()
    message= other.stat_message(
            user_id=msg.chat.id,
            action_list=[],
            period='today',
            split='by actions'
        )
    await msg.answer(f"{message}", reply_markup=stat_menu(period='today', split='by actions', list_actions=[]),
                     parse_mode=html)
    
@dp.message_handler(commands=['focus'], state="*")
async def focus_message(msg: Message, state: FSMContext):
    await state.finish()
    try:
        str_dt= msg.text[7:] + f".{date.today().year}"
        dt= datetime.strptime(str_dt, '%d.%m.%Y').strftime('%Y-%m-%d')
        await state.update_data(date=dt)
    except  Exception as ex:
        db.usefulles_user(msg.chat.id)
        print(ex)
    finally:
        messages= ""
        if db.count_logs(msg.chat.id) == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
        await msg.answer(f"{messages}",
                         reply_markup= action_menu(msg.chat.id),
                        parse_mode=html)
        await Focus.action.set()
        
        
        
        
        
@dp.message_handler(commands=['friends'], state='*')
@dp.message_handler(commands=['friends'])
async def friends_message(msg: Message, state: FSMContext):
    await state.finish()
    if db.get_friends(msg.chat.id) is False:
        await msg.answer(f"You don't have any friends yet. Add them!", reply_markup=add_friend_button)
    else: 
        friend_id= db.get_friends(msg.chat.id)[0][0]
        await msg.answer(text=other.stat_friend(friend_id=friend_id, user_id=msg.chat.id),
                                  reply_markup=next_menu(i=0, user_id=msg.chat.id), parse_mode=html)