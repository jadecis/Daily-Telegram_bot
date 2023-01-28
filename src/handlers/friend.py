from loader import dp, db, Friend, bot, html
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from src.keyboards.inline.other import add_friend_button, friends_menu, add_friends_menu, add_markup, rej_markup
from src.keyboards.inline.other import show_friend_button, next_menu
from src.handlers import other
    
@dp.callback_query_handler(text= 'friend')
async def friend_answer(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Write a friend's username (example: '@my_best_friend')")
    await Friend.name.set()

@dp.callback_query_handler(text= 'friend')
async def friend_answer(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Write a friend's username (example: '@my_best_friend')")
    await Friend.name.set()

@dp.callback_query_handler(text_contains= 'next_')
async def next_answer(call: CallbackQuery, state: FSMContext):
    i = int(call.data[5:])
    count_fr= len(db.get_friends(call.message.chat.id))-1
    i=0 if i== count_fr else i+1
    friend_id= db.get_friends(user_id= call.message.chat.id)[i][0]
    await call.message.edit_text(text=other.stat_friend(friend_id=friend_id, user_id=call.message.chat.id),
                                 reply_markup=next_menu(i=i, user_id=call.message.chat.id),
                                 parse_mode=html)
 

@dp.message_handler(content_types=['text'], state=Friend.name)
async def name_handler(msg: Message, state: FSMContext):
    friend_id= db.find_id(msg.text[1:])
    if friend_id[0] is False:
        await msg.answer(f"Friend not found!\nPlease, write username who using this bot!!!")
        await Friend.name.set()
    elif friend_id[0] == msg.chat.id:
        await msg.answer(f"You can't add yourself!\nPlease, write username other friend!")
        await Friend.name.set()
    else:
        res= db.can_add_friend(
            user_id=msg.chat.id,
            friend_id=friend_id[0]
        )
        if res:
            try:
                await bot.send_message(chat_id=friend_id[0],
                                    text=f"🙋 @{msg.chat.username} wants to add you to friends. If you agree, you will be able to see each other's stats.",
                                    reply_markup= add_friends_menu(user_name=msg.chat.username))
            except Exception as ex:
                print(ex)
                            
            await msg.answer(f"✅ Ready! {msg.text} has received a friend request and needs to confirm it. After confirmation, the friend will appear in the friends section",
                             reply_markup=friends_menu)
            await state.finish()
        else:
            await msg.answer(f"Friend have already been added!!!\nPlease, write username other friend!")
            await Friend.name.set()
            
@dp.callback_query_handler(text_contains= 'submit_')
async def to_answer(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    user_name= call.data.split('_')[2]
    user_id= db.find_id(user_name)[0]
    if call.data.split('_')[1] == 'rej':
        await call.message.answer(text=f"🙅 You rejected the application of @{user_name}", reply_markup=add_markup(user_name))
    elif call.data.split('_')[1] == 'add':
        db.add_friend(
            user_id=user_id,
            friend_id=call.message.chat.id
        )
        await call.message.answer(text=f"💁 @{user_name} is now your friend. You can see his data in the section /friends", reply_markup=rej_markup(user_name))
        await bot.send_message(chat_id=user_id, text=f"🎉 @{call.message.chat.username} has accepted your friend offer! Now you can see his stats!", reply_markup=show_friend_button)
        
@dp.callback_query_handler(text_contains= 'change_')
async def change_answer(call: CallbackQuery, state: FSMContext):
    user_name= call.data.split('_')[2]
    user_id= db.find_id(user_name)[0]
    if call.data.split('_')[1] == 'rej':
        db.del_friend(
            user_id=call.message.chat.id,
            friend_id=user_id
        )
        await call.message.edit_text(text=f"🙅 You rejected the application of @{user_name}")
    elif call.data.split('_')[1] == 'add':
        db.add_friend(
            user_id=user_id,
            friend_id=call.message.chat.id
        )
        await call.message.edit_text(text=f"💁 @{user_name} is now your friend. You can see his data in the section /friends", reply_markup=rej_markup(user_name))
        await bot.send_message(chat_id=user_id, text=f"🎉 @{call.message.chat.username} has accepted your friend offer! Now you can see his stats!", reply_markup=show_friend_button)