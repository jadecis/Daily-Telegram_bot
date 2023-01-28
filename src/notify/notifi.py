from loader import db, dp, html, bot
from datetime import date, timedelta
import asyncio
import aioschedule
from src.keyboards.inline.focus import log_button


#Notification
async def every_mon():
    for user_id in db.user_info_id():
        try:
            await bot.send_message(chat_id=user_id[0], text=f"🎉 It was a great week!\nYou got ⭐️ <b>{int(db.get_points_atweek(user_id[0])[0])}</b> for this 7 days",
                                   parse_mode=html)
        except Exception as ex:
            pass
        
async def every_day():
    for user_id in db.user_info_id():
        if db.stat_today(user_id=user_id[0]):
            if int(db.user_info(user_id[0])[3]) != 0:
                try:
                    await dp.bot.send_message(chat_id=user_id[0], text=f"🤜🤛 Just do it! You have shock mode 🔥{int(db.user_info(user_id[0])[3])} days. Don't lose it!",
                                              parse_mode=html,
                                              reply_markup=log_button)
                except:
                    pass
        else:
            if int(db.user_info(user_id[0])[3]) != 0: 
                try:
                    await dp.bot.send_message(chat_id=user_id[0], text=f"🤜🤛 Just do it! You have shock mode 🔥{int(db.user_info(user_id[0])[3])} days. Don't lose it!",
                                              parse_mode=html,
                                              reply_markup=log_button)
                except:
                    pass
                
async def check_shoke():
    for user_id in db.user_info_id():
        if len(db.stat_today(user_id=user_id[0], date=date.today()- timedelta(1))) != 0:
            db.shoke_user(user_id=user_id[0])
        else:
            db.shoke_user(user_id=user_id[0], sk=False)

async def scheduler():
    aioschedule.every().monday.at("10:00").do(every_mon)
    aioschedule.every().day.at("11:00").do(check_shoke)
    #aioschedule.every().minute.do(every_mon)
    aioschedule.every().day.at("12:00").do(every_day)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
