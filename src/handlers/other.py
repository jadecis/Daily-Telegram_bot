from loader import db 
from math import floor
from datetime import timedelta, date, datetime
import calendar


def stat_message(user_id, action_list, period, split):
    count_skip=db.skip_info(user_id)
    star= db.usefulles_user(user_id)
    zero_point= False
    categories =True
    if (count_skip > 0 and count_skip < 8) and star is True:
        categories= True
        zero_point= True
    elif count_skip == 0:
        categories= True
        zero_point= False
    else:
        categories =False
    message=""
    if period== 'today':
        dt=date.today().strftime('%Y-%m-%d')
        result= db.stat_today(user_id, dt)
        print(result)
        print(f'[#] {dt}')        
        message+=f"🗓 {date.today().strftime('%a, %d.%m')}\n"
        decimal=1
    elif period== 'week':
        decimal=1
        if split == 'by action':
            first_date= date.today()- timedelta(days= date.today().weekday())
            second_date= first_date + timedelta(weeks=1)
            result= db.stat_by_interval(user_id=user_id, first_date=first_date, second_date=second_date)
            message+=f"🗓 Week {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}\n" 
        else:
            first_date= date.today() - timedelta(7)
            second_date= date.today() + timedelta(1)
            message+=f"🗓 Week {first_date.strftime('%d.%m')} — {date.today().strftime('%d.%m')}\n"
            result= db.stat_by_interval(user_id=user_id, first_date=first_date, second_date=second_date)
    elif period== 'month':
        decimal=0
        if split == 'by action':
            first_date= date(year=date.today().year, month=date.today().month, day=1)#.today()- timedelta(days= date.today().weekday())
            days_in_month = calendar.monthrange(year=date.today().year, month=date.today().month)[1]
            second_date= first_date + timedelta(days=days_in_month)
            result= db.stat_by_interval(user_id=user_id, first_date=first_date, second_date=second_date)
            message+=f"🗓 Month {first_date.strftime('%d.%m')} — {(second_date-timedelta(1)).strftime('%d.%m')}\n"
        else:
            first_date= date.today()- timedelta(days= date.today().weekday()) - timedelta(weeks=4)
            second_date= date.today() + timedelta(days=(6-date.today().weekday()))
            message+=f"🗓 Month {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}\n"
            result= db.stat_by_interval(user_id=user_id, first_date=first_date, second_date=second_date)
    elif period== 'all':
        decimal=0
        old= datetime.strptime(db.first_log(user_id)[0], '%Y-%m-%d').date()
        first_date=  old - timedelta(days=old.weekday())     
        second_date= date.today() + timedelta(days=(7-date.today().weekday()))
        second_date= date.today()
        result= db.stat_by_interval(user_id=user_id, first_date=first_date, second_date=second_date)
        
        message+=f"🗓 All time {first_date.strftime('%d.%m')} — {second_date.strftime('%d.%m')}\n"
    if result:
        if split == 'by records':
            message+=stat_Byrecords(
                action_list=action_list,
                result=result,
                cat=categories,
                zero_point=zero_point
            )
        elif split == 'by day':
            message+= stat_Byday(
                action_list=action_list,
                first_date=first_date,
                second_date= second_date,
                zero_point=zero_point,
                user_id=user_id,
                cat=categories
            )
        elif split == 'by week':
            message+= stat_Byweek(
                action_list=action_list,
                first_date=first_date,
                second_date= second_date,
                zero_point=zero_point,
                user_id=user_id,
                cat=categories
            )
        else:
            message+= stat_Byaction(
                    action_list=action_list,
                    result=result,
                    decimal=decimal,
                    cat=categories,
                    zero_point=zero_point
                )
    else:
        message +="\nYou haven't been active or you haven't been active this action during this interval of time"
    return message

def stat_Byaction(action_list, result, decimal, zero_point, cat =True):
    points = {}
    hours = {}  
    min_value = 1 if decimal == 0 else 0.1
    message=""
    total_hours= 0.0
    total_points= 0.0
    if action_list:
        for stat in result:
            if action_list.__contains__(stat[0]):
                if stat[0] in points or stat[0] in hours:
                    points[stat[0]]+= stat[2]
                    hours[stat[0]]+= stat[1]
                else:
                    points[stat[0]]= stat[2]
                    hours[stat[0]]= stat[1]
    else:
        for stat in result:
            
            if stat[0] in points:
                points[stat[0]]+= stat[2]
                hours[stat[0]]+= stat[1]
            else:
                points[stat[0]]= stat[2]
                hours[stat[0]]= stat[1]
    if cat:
        for name in hours:
            total_hours+= hours[name]
            total_points+= points[name]
            act_hour= (floor((hours[name]- int(hours[name])) * 10))/10 + int(hours[name]) if decimal == 1 else int(hours[name])
            act_hour= f'&lt;{min_value}' if act_hour < min_value else act_hour
            point= 0 if zero_point is True else int(points[name])
            message+= f"\n{name} 🕝{act_hour}/ ⭐️{point}"
        total_hours= (floor((total_hours- int(total_hours)) * 10))/10 + int(total_hours) if decimal == 1 else int(total_hours)
        total_hours= f'&lt;{min_value}' if total_hours < min_value and total_hours != 0 else total_hours
        totalpoint= 0 if zero_point is True else int(total_points)
        message+= f"\n\n<b>Total</b>: 🕝{total_hours}/ ⭐️{int(totalpoint)}"
    else:
        for name in hours:
            total_hours+= hours[name]
            act_hour= (floor((hours[name]- int(hours[name])) * 10))/10 + int(hours[name]) if decimal == 1 else int(hours[name])
            act_hour= f'&lt;{min_value}' if act_hour < min_value else int(act_hour)
            message+= f"\n{name} 🕝{act_hour}"
        total_hours= (floor((total_hours- int(total_hours)) * 10))/10 + int(total_hours) if decimal == 1 else int(total_hours)
        total_hours= f'&lt;{min_value}' if total_hours < min_value and total_hours != 0 else total_hours
        message+= f"\n\n<b>Total</b>: 🕝{total_hours}"
        
    return message

def stat_Byrecords(action_list, result, zero_point, cat =True):
    message=""
    if action_list:
        for stat in result:
            if list(action_list).__contains__(stat[0]):
                duration= f'({stat[4]})' if stat[4] != None else ""
                hour= '&lt;0.1' if stat[1] > 0 and stat[1] < 0.1 else (floor((stat[1]- int(stat[1])) * 10))/10 + int(stat[1])
                if cat:
                    point= 0 if zero_point is True else int(stat[2])
                    message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} / ⭐️{point} {duration}"
                else:
                    message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} {duration}"
    else:
        for stat in result:
            duration= f'({stat[4]})' if stat[4] != None else ""
            hour= '&lt;0.1' if stat[1] > 0 and stat[1] < 0.1 else (floor((stat[1]- int(stat[1])) * 10))/10 + int(stat[1])
            if cat:
                point= 0 if zero_point is True else int(stat[2])
                message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} / ⭐️{point} {duration}"
            else:

                message+=f"\n{stat[0]} / {stat[3]} 🕝{hour} {duration}"
    
    return message

def stat_Byday(action_list, first_date, second_date, zero_point, user_id, cat =True):
    message= ""
    top ={}
    prise=""
    while first_date < second_date:
        result= db.stat_today(user_id=user_id, date=first_date)
        total_hours = 0.0
        total_points = 0.0
        for stat in result:
            if len(action_list) != 0:
                if list(action_list).__contains__(stat[0]):
                    total_hours+= stat[1]
                    total_points+=stat[2]
            else:
                total_hours+= stat[1]
                total_points+=stat[2]
        top[first_date]= {'hour' : total_hours, 'point' : total_points}
        first_date += timedelta(1)
    sort_top= sorted(top.items(), key=lambda x: x[1].get('point'), reverse=True)
    for key in top:
        prise= ""
        point= 0 if zero_point is True else int(top[key]['point'])
        if point != 0:
            if sort_top[0][0] == key and sort_top[0][1].get('point') == top[key].get('point') and top[key].get('point') != 0:
                prise= "🥇" 
            elif sort_top[1][0] == key and sort_top[1][1].get('point') == top[key].get('point') and top[key].get('point') != 0:
                prise= "🥈"
            elif sort_top[2][0] == key and sort_top[2][1].get('point') == top[key].get('point') and top[key].get('point') != 0:
                prise= "🥉"
            else:
                prise= ""
        hours= '&lt;0.1' if top[key]['hour'] > 0 and top[key]['hour'] < 0.1 else (floor((top[key]['hour']-int(top[key]['hour'])) * 10))/10 +int(top[key]['hour'])
        if cat:
            message+= f"\n{key.strftime('%a')} 🕝{hours} / ⭐️{point} {prise}"
        else:
            message+= f"\n{key.strftime('%a')} 🕝{hours} {prise}"
    return message

def stat_Byweek(action_list, first_date, second_date, zero_point, user_id, cat =True):
    message= ""
    top= {}
    prise=''
    while first_date < second_date:
        total_hours= 0.0
        total_points= 0.0
        result= db.stat_by_interval(user_id=user_id, first_date=first_date, second_date=first_date+ timedelta(days=6))
        
        if len(action_list) != 0:
            for stat in result:
                if list(action_list).__contains__(stat[0]):
                    total_hours+=stat[1]
                    total_points+= stat[2]
        else:
            for stat in result:
                total_hours+=stat[1]
                total_points+= stat[2]
        top[first_date]= {'hour' : total_hours, 'point' : total_points}
        first_date += timedelta(weeks=1)
    sort_top= sorted(top.items(), key=lambda x: x[1].get('point'), reverse=True)
    for key in top:
        prise= ""
        point= 0 if zero_point is True else int(top[key]['point'])
        if point != 0:
            if sort_top[0][0] == key and sort_top[0][1].get('point') == top[key].get('point') and sort_top[0][1].get('point') != 0:
                prise= "🥇" 
            elif sort_top[1][0] == key and sort_top[1][1].get('point') == top[key].get('point') and sort_top[1][1].get('point') != 0:
                prise= "🥈"
            elif sort_top[2][0] == key and sort_top[2][1].get('point') == top[key].get('point') and sort_top[2][1].get('point') != 0:
                prise= "🥉"
            else:
                prise= ""
        hours= '&lt;1' if (top[key]['hour'] > 0) and (top[key]['hour'] < 1) else int(top[key]['hour'])
        if cat:
            
            message+=f"\n{key.strftime('%d-%b')} 🕝{hours}/ ⭐️{point} {prise}"
        else:
            message+=f"\n{key.strftime('%d-%b')} 🕝{hours} {prise}"
               
    return message

def stat_friend(friend_id, user_id):
    count_skip=db.skip_info(user_id)
    star= db.usefulles_user(user_id)
    zero_point= False
    categories =True
    if (count_skip > 0 and count_skip < 8) and star is True:
        categories= True
        zero_point= True
    elif count_skip == 0:
        categories= True
        zero_point= False
    else:
        categories =False
    
    
    today= date.today()
    monday= date.today()- timedelta(days= date.today().weekday())
    first_day= date(year=date.today().year, month=date.today().month, day=1)
    days_in_month = calendar.monthrange(year=date.today().year, month=date.today().month)[1]
    old= db.first_log(friend_id)[0].split('-') if db.first_log(friend_id)[0] != None else date.today().strftime('%Y-%m-%d').split('-')
    old_date_friend=  date(year=int(old[0]), month=int(old[1]), day=int(old[2]))
    old= db.first_log(user_id)[0].split('-') if db.first_log(user_id)[0] != None else date.today().strftime('%Y-%m-%d').split('-')
    old_date=date(year=int(old[0]), month=int(old[1]), day=int(old[2]))
    week= [monday, monday+timedelta(days=6)]
    month= [first_day, first_day+timedelta(days=days_in_month)- timedelta(days=1)]
    all_friend= [old_date_friend, today]
    all= [old_date, today]

    today_friend=db.stat_short_today(user_id=friend_id) if db.stat_short_today(user_id=friend_id) != tuple([None, None]) else [0,0]
    today_me=db.stat_short_today(user_id=user_id) if db.stat_short_today(user_id=user_id) != tuple([None, None]) else [0,0]

    stat_week_friend= db.get_short_stat(user_id=friend_id, first_date= week[0], second_date= week[1]) if db.get_short_stat(user_id=friend_id, first_date= week[0], second_date= week[1]) != tuple([None, None]) else [0,0]
    stat_week= db.get_short_stat(user_id=user_id, first_date= week[0], second_date= week[1]) if db.get_short_stat(user_id=user_id, first_date= week[0], second_date= week[1]) != tuple([None, None]) else [0,0]
    
    stat_month_friend= db.get_short_stat(user_id=friend_id, first_date= month[0], second_date= month[1]) if db.get_short_stat(user_id=friend_id, first_date= month[0], second_date= month[1]) != tuple([None, None]) else [0,0]
    stat_month= db.get_short_stat(user_id=user_id, first_date= month[0], second_date= month[1]) if db.get_short_stat(user_id=user_id, first_date= month[0], second_date= month[1]) != tuple([None, None]) else [0,0]

    stat_all_friend= db.get_short_stat(user_id=friend_id, first_date= all_friend[0], second_date= all_friend[1]) if db.get_short_stat(user_id=friend_id, first_date= all_friend[0], second_date= all_friend[1]) != tuple([None, None]) else [0,0]
    stat_all= db.get_short_stat(user_id=user_id, first_date= all[0], second_date= all[1]) if db.get_short_stat(user_id=user_id, first_date= all[0], second_date= all[1]) != tuple([None, None]) else [0,0]
    
    today_hour_fr= '&lt;0.1' if today_friend[0] > 0 and today_friend[0] < 0.1 else (floor((today_friend[0]-int(today_friend[0])) * 10))/10 + int(today_friend[0])
    today_hour_me= '&lt;0.1' if today_me[0] > 0 and today_me[0] < 0.1 else (floor((today_me[0]- int(today_me[0])) * 10))/10+ int(today_me[0])
    
    week_fr= '&lt;0.1' if stat_week_friend[0] > 0 and stat_week_friend[0] < 0.1 else (floor((stat_week_friend[0]-int(stat_week_friend[0])) * 10))/10+ int(stat_week_friend[0])
    week_me= '&lt;0.1' if stat_week[0] > 0 and stat_week[0] < 0.1 else (floor((stat_week[0]-int(stat_week[0])) * 10))/10+ int(stat_week[0])

    month_fr= '&lt;1' if stat_month_friend[0] > 0 and stat_month_friend[0] < 1 else int(stat_month_friend[0])
    month_me= '&lt;1' if stat_month[0] > 0 and stat_month[0] < 1 else int(stat_month[0])
    
    all_fr= '&lt;1' if stat_all_friend[0] > 0 and stat_all_friend[0] < 1 else int(stat_all_friend[0])
    all_me= '&lt;1' if stat_all[0] > 0 and stat_all[0] < 1 else int(stat_all[0])
    
    if categories is True:
        if zero_point is True:   
            message=f"""
🙋 @{db.user_info(friend_id)[2]}
Day 🕝{today_hour_fr} / ⭐️{int(today_friend[1])} (you: 🕝{today_hour_me} / ⭐️{int(today_me[1])})
Week 🕝{week_fr} / ⭐️{int(stat_week_friend[1])} (you: 🕝{week_me} / ⭐️{int(stat_week[1])})
Month 🕝{month_fr} / ⭐️{int(stat_month_friend[1])} (you: 🕝{month_me} / ⭐️{int(stat_month[1])})
All 🕝{all_fr} / ⭐️{int(stat_all_friend[1])} (you: 🕝{all_me} / ⭐️{int(stat_all[1])})
"""
        else:
            message=f"""
🙋 @{db.user_info(friend_id)[2]}
Day 🕝{today_hour_fr} / ⭐️{int(today_friend[1])} (you: 🕝{today_hour_me} / ⭐️0)
Week 🕝{week_fr} / ⭐️{int(stat_week_friend[1])} (you: 🕝{week_me} / ⭐️0)
Month 🕝{month_fr} / ⭐️{int(stat_month_friend[1])} (you: 🕝{month_me} / ⭐️0)
All 🕝{all_fr} / ⭐️{int(stat_all_friend[1])} (you: 🕝{all_me} / ⭐️0)
"""
    else:
                message=f"""
🙋 @{db.user_info(friend_id)[2]}
Day 🕝{today_hour_fr} (you: 🕝{today_hour_me})
Week 🕝{week_fr} (you: 🕝{week_me})
Month 🕝{month_fr} (you: 🕝{month_me})
All 🕝{all_fr} (you: 🕝{all_me})
"""
    return message