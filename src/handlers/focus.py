from loader import db, dp, html, Focus
from aiogram.dispatcher import FSMContext
from src.keyboards.inline.focus import action_menu, log_menu, categories_menu, record_menu, focus_menu, stop_menu, not_today_menu, add_button
from src.keyboards.reply.main_button import menu_markup
from aiogram.types import Message, CallbackQuery
from datetime import datetime, date
from math import floor
import aiogram


@dp.callback_query_handler(text= 'record',)
async def record_answer(call: CallbackQuery, state: FSMContext):
    messages= ""
    if db.count_logs(call.message.chat.id) == 0:
        messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
    else:
        messages="Select or type <b>activity</b>🏄‍♂️"
    await call.message.answer(f"{messages}",
                        reply_markup= action_menu(call.message.chat.id),
                    parse_mode=html)
    await Focus.action.set()

@dp.message_handler(content_types=['text'], state=Focus.action)
async def name_action(msg: Message, state: FSMContext):
    try:
        await state.update_data(action=str(msg.text))
        if (db.skip_info(msg.chat.id) >= 8 and db.usefulles_user(msg.chat.id) is True) or (db.skip_info(msg.chat.id) >= 4 and db.usefulles_user(msg.chat.id) is False):
            await msg.answer(f"🏄‍♂️ {msg.text}\n\nStart recording or have you already performed the action?",
                                reply_markup=log_menu,
                                parse_mode=html)
            await Focus.log.set()
        else:
            await msg.answer(f"🏄‍♂️{msg.text}\n\nSelect the level of 🚦<b>usefulness</b> of activity",
                                reply_markup=categories_menu(),
                                parse_mode=html)
            await Focus.category.set()
    except aiogram.utils.exceptions.CantParseEntities:
        await msg.answer(f"Please, don't type this symbol: '<, >, &' ")
        
@dp.callback_query_handler(text_contains= 'act_', state=Focus.action)
async def act_answer(call: CallbackQuery, state: FSMContext):
    act= call.data.split('_')[1]
    try:
        await state.update_data(action=act)
        if (db.skip_info(call.message.chat.id) >= 8 and db.usefulles_user(call.message.chat.id) is True) or (db.skip_info(call.message.chat.id) >= 4 and db.usefulles_user(call.message.chat.id) is False):
            await call.message.edit_text(f"🏄‍♂️ {act}\n\nStart recording or have you already performed the action?",
                                         reply_markup=log_menu,
                                         parse_mode=html)
            await Focus.log.set()
        else:
            await call.message.edit_text(f"🏄‍♂️{act}\n\nSelect the level of 🚦<b>usefulness</b> of activity",
                                         reply_markup=categories_menu(),
                                         parse_mode=html)
            await Focus.category.set()
    except aiogram.utils.exceptions.CantParseEntities:
        await call.message.answer(f"Please, don't type this symbol: '<, >, &' ")
        await Focus.action.set()
           
@dp.callback_query_handler(text_contains= 'cat_', state=Focus.category)
async def cat_answer(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cat= call.data.replace('cat_', '')
    act= data.get('action')
    if cat== 'Skip':
        db.skip_user(call.message.chat.id)
        await call.message.edit_text(f"🏄‍♂️ {act}\n\nStart recording or have you already performed the action?", 
                                     reply_markup=log_menu, 
                                     parse_mode=html)
    else:
        await state.update_data(category=cat)
        db.skip_user(call.message.chat.id, sk=False)
        await call.message.edit_text(f"🏄‍♂️ {act} /🚦{cat.split('_')[0]} useful\n\nStart recording or have you already performed the action?",
                                     reply_markup=log_menu,
                                     parse_mode=html)
    await Focus.log.set()
    
@dp.callback_query_handler(text_contains= 'log_', state=Focus.log)
async def log_answer(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    act= data.get('action') 
    cat= f" /🚦 {data.get('category').split('_')[0]} useful" if data.get('category') != None else ""
    if call.data == 'log_enter':
        await call.message.edit_text(f"🏄‍♂️ {act}{cat}\n\nEnter duration🕝 (example: 1,5 or 1:30)",
                                     parse_mode=html)
        await Focus.enter.set()
    if call.data == "log_start":
        data = await state.get_data()
        start_date= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        category = '' if data.get('category') == None else f" /🚦{data.get('category').split('_')[0]} useful"
        act= data.get('action')
        await state.update_data(rec_date=start_date)
        await state.update_data(start_dur_date=start_date)
        await call.message.edit_text(f"⏳ Recording...\n 🏄‍♂️ {act}{category}\nMay the focus be with you! 🧘‍♂️", reply_markup=record_menu)
        
@dp.callback_query_handler(text_contains= 'rec_', state=Focus.log)
async def rec_answer(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category= f" /🚦{data.get('category').split('_')[0]} useful" if data.get('category') != None else ""
    act= data.get('action')
    if call.data== 'rec_stop':
        start_dur= datetime.strptime(data.get('start_dur_date'), '%Y-%m-%d %H:%M:%S')  
        stop_dur= datetime.now() if data.get('stop_dur_date') == None else data.get('stop_dur_date')
        
        start_date= datetime.strptime(data.get('rec_date'), '%Y-%m-%d %H:%M:%S') 
        stop_date= datetime.now()
        if data.get('time_stop') != None and data.get('resume') == None:
            time=float(data.get('time_stop'))
        elif data.get('time_stop') != None and data.get('resume') == True:
            time=float(data.get('time_stop')) + (stop_date- start_date).total_seconds() / 3600
        else:
            time= (stop_date- start_date).total_seconds() / 3600
        if data.get('category') == None:
            cat=""
            multi= 0
        else:
            cat= data.get('category').split('_')[0]
            multi= int(data.get('category').split('_')[1])
        point= multi * time
        hour= '&lt;0.1' if time < 0.1 and time > 0 else time
        if type(hour) == float:
            if hour == 1.2:
                hour= 1.2
            elif int(hour) >= 1:
                hour= (floor((hour- int(hour)) * 10))/10+ int(hour)
            else:
                hour=(floor(hour * 10))/10+ int(hour)
        duration= f"{start_dur.strftime('%H:%M')} - {stop_dur.strftime('%H:%M')}"

        key= db.add_focus(
            user_id=call.message.chat.id,
            action=act,
            hour=time,
            date=date.today(),
            category=cat,
            point=point,
            duration=duration
            )
        count_skip=db.skip_info(call.message.chat.id)
        star= db.usefulles_user(call.message.chat.id)
        if (count_skip > 0 and count_skip < 8) and star is True:
            messages=f"{duration}\n🎉 Added 🕝{hour} / ⭐️0\n🏄‍♂️ {act}{category}"
        elif count_skip == 0:
            messages=f"{duration}\n🎉 Added 🕝{hour} / ⭐️{int(point)}\n🏄‍♂️ {act}{category}"
        else:
            messages=f"{duration}\n🎉 Added 🕝{hour}\n🏄‍♂️ {act}{category}"
        await call.message.edit_text(f"{messages}", parse_mode=html, reply_markup=focus_menu(key=key))
        
        if db.count_logs(user_id=call.message.chat.id) == 1:
            await call.message.answer(f"It's your first focus!🔥 Good job!\nUse the buttons below for record activity and show statistics",
                                      reply_markup= menu_markup,
                                      parse_mode=html)
        await state.finish()
    if call.data== 'rec_pause':
        start_date= datetime.strptime(data.get('rec_date'), '%Y-%m-%d %H:%M:%S') 
        stop_date= datetime.now()
        time= (stop_date- start_date).total_seconds() / 3600
        await state.update_data(time_stop= time)
        await state.update_data(stop_dur_date= datetime.now())
        await call.message.edit_text(f"⏸ On pause\n🏄‍♂️ {act}{category}\nMay the focus be with you! 🧘‍♂️", 
                                     parse_mode=html, 
                                     reply_markup=stop_menu)
    if call.data== 'rec_resume':
        start_date= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await state.update_data(rec_date=start_date)
        await state.update_data(resume=True)
        await state.update_data(stop_dur_date= None)
        await call.message.edit_text(f"⏳ Recording...\n 🏄‍♂️ {act}{category}\nMay the focus be with you! 🧘‍♂️",
                                     reply_markup=record_menu)
        
@dp.message_handler(content_types=['text'], state=Focus.enter)
async def text_q3_answer(msg: Message, state: FSMContext):
    try:
        if msg.text.__contains__(':'):
            float(msg.text.replace(':', '.'))
            time= msg.text.split(':')
            hours= float(int(time[0].strip()) + float(time[1].strip()) / 60)
        elif msg.text.__contains__(','):
            hours= float(msg.text.replace(',', '.'))
        else:
            hours= float(msg.text)
    
    except Exception as ex:
        print(ex)
        await msg.answer(f"Your duration is not invalid!\nPlease, type me new duration (example: 1,5 or 1:30)")
        await Focus.enter.set()
        return
    
    data = await state.get_data()

    date_log= date.today() if data.get('date') == None else datetime.strptime(data.get('date'), '%Y-%m-%d')
    await state.update_data(date=date_log)
    category = '' if data.get('category') == None else data.get('category').split('_')[0]
    act= data.get('action')
    print(type(act))
    
    if data.get('category') == None:
        multi= 0
        cat= ""
        category=""
    else:
        category= f" /🚦{category} useful"
        multi= int(data.get('category').split('_')[1])
        cat= data.get('category').split('_')[0]
    point= multi * hours
    
    key= db.add_focus(
        user_id=msg.chat.id,
        action=f"{str(act)}",
        hour=hours,
        date=date_log.strftime('%Y-%m-%d'),
        category=cat,
        point=point
        )
    view_date= "" if data.get('date') == None else date_log.strftime('%a, %d.%m')
    hours= '&lt;0.1' if hours < 0.1 and hours > 0 else hours#(floor(hours * 10))/10+ int(hours)
    
    if type(hours) == float:
        if hours == 1.2:
            hours= 1.2
        elif int(hours) >= 1:
            hours= (floor((hours- int(hours)) * 10))/10+ int(hours)
        else:
            hours=(floor(hours * 10))/10+ int(hours)
    elif type(hours) == int:
        hours= int(hours)
    
    count_skip=db.skip_info(msg.chat.id)
    star= db.usefulles_user(msg.chat.id)
    if (count_skip > 0 and count_skip < 8) and star is True:
        messages=f"{view_date}\n🎉 Added 🕝{hours} / ⭐️0\n🏄‍♂️{act}{category}"
    if count_skip == 0:
        messages=f"{view_date}\n🎉 Added 🕝{hours} / ⭐️{int(point)}\n 🏄‍♂️{act}{category}"
    else:
        messages=f"{view_date}\n🎉 Added 🕝{hours}\n 🏄‍♂️{act}{category}"
    
    if date_log.strftime('%Y.%d.%m') == date.today().strftime('%Y.%d.%m'):
        await msg.answer(f"{messages}", reply_markup= focus_menu(key=key),
                         parse_mode=html)
        if db.count_logs(user_id=msg.chat.id) == 1:
            await msg.answer(f"It's your first focus!🔥 Good job!\nUse the buttons below for record activity and show statistics",
                             reply_markup= menu_markup,
                             parse_mode=html)
    else:
        await msg.answer(f"{messages}", reply_markup=not_today_menu(date_log.strftime('%d.%m'), key=key),
                         parse_mode=html)
        
        if db.count_logs(user_id=msg.chat.id) == 1:
            await msg.answer(f"It's your first focus!🔥 Good job!\nUse the buttons below for record activity and show statistics",
                             reply_markup= menu_markup,
                             parse_mode=html)
    await state.finish()

@dp.callback_query_handler(text_contains= 'foc_', state="*")
async def foc_answer(call: CallbackQuery, state: FSMContext):
    await state.finish()
    if call.data.__contains__( 'foc_del'):
        key= call.data.split('_')[2]
        log= db.del_logByKey(int(key))
        hour= float(log[4])
        category= log[3]
        act= log[2]
        point= log[5]
        time= '&lt;0.1' if hour < 0.1 and hour > 0 else floor((hour-int(hour)) * 10)/10+ int(hour)
        category= f" /🚦{category} useful" if category != "" else ""
        count_skip=db.skip_info(call.message.chat.id)
        star= db.usefulles_user(call.message.chat.id)
        if (count_skip > 0 and count_skip < 8) and star is True:
            messages=f"🚮 Deleted 🕝{time} / ⭐️0\n🏄‍♂️{act}{category}"
        if count_skip == 0:
            messages=f"🚮 Deleted 🕝{time} / ⭐️{int(point)}\n🏄‍♂️{act}{category}"
        else:
            messages=f"🚮 Deleted 🕝{time}\n🏄‍♂️{act}{category}"
        await call.message.delete()
        await call.message.answer(f"{messages}", reply_markup=add_button, parse_mode=html)
        await state.finish()
    
    if call.data== 'foc_add':
        messages= ""
    
        if db.count_logs(user_id=call.message.chat.id) == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
    
        await call.message.answer(f"{messages}", 
                                  reply_markup=action_menu(user_id=call.message.chat.id), 
                                  parse_mode=html)
        await state.finish()
        await Focus.action.set()
               
@dp.callback_query_handler(text_contains= 'not_', state='*')
async def not_answer(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)   
    if call.data == 'not_td':
        await state.update_data(date=None)
        messages= ""
    
        if db.count_logs(user_id=call.message.chat.id) == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
    
        await call.message.answer(f"{messages}", 
                                  reply_markup=action_menu(user_id=call.message.chat.id),
                                  parse_mode=html)
        await Focus.action.set()
    else:
        year= date.today().year
        dt= datetime.strptime(f"{call.data.split('_')[2]}.{year}", '%d.%m.%Y').strftime("%Y-%m-%d") 
        await state.update_data(date=dt)
        messages= ""
    
        if db.count_logs(user_id=call.message.chat.id) == 0:
            messages='Type name of new <b>activity</b>🏄‍♂️\nFor example: "Work", "Sport", etc.'
        else:
            messages="Select or type <b>activity</b>🏄‍♂️"
    
        await call.message.answer(f"{messages}", 
                                    reply_markup=action_menu(user_id=call.message.chat.id),
                                  parse_mode=html)
        await Focus.action.set()
        
        

    
    