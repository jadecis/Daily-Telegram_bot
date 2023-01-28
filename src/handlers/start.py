from loader import Focus, html, dp, db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from src.handlers import other
from src.keyboards.inline.stats import stat_menu
from src.keyboards.inline.focus import  action_menu




@dp.message_handler(Text(equals=['Record activity', 'Show statistics']), state='*')
async def text_answer(msg: Message, state: FSMContext):
    await state.finish()
    if msg.text == 'Record activity':
        message= ""
        if db.count_logs(msg.chat.id) == 0:
            message='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            message="Select or type <b>activity</b>🏄‍♂️"
        await msg.answer(f"{message}", reply_markup=action_menu(user_id=msg.chat.id), parse_mode=html)
        await Focus.action.set()
    elif msg.text == 'Show statistics':
        message= other.stat_message(
            user_id=msg.chat.id,
            action_list=[],
            period='today',
            split='by actions'
        )
        await msg.answer(f"{message}", reply_markup=stat_menu(period='today', split='by actions', list_actions=[]),
                     parse_mode=html)
    