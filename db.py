import sqlite3
from datetime import datetime, timedelta
from datetime import date as dt

class Databae():
    def __init__(self, db_file):
        self.connection= sqlite3.connect(db_file)
        self.cursor= self.connection.cursor()
        
    def stat_by_interval(self, user_id, first_date, second_date):
        with self.connection:
            res= self.cursor.execute("SELECT `action`, `hour`, `point` FROM `logs` WHERE `user_id` = ? and (`date` >= ? and `date` < ?)",(user_id, first_date, second_date,) ).fetchall()
            return res
        
    def stat_today(self, user_id, date):
        with self.connection:
            res= self.cursor.execute("SELECT `action`, `hour`, `point`, `category`, `duration` FROM logs WHERE user_id= ? and `date` = ?", (user_id, date, )).fetchone()
            return res
        
    def first_log(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT MIN(`date`) FROM logs WHERE user_id= ?", (user_id, )).fetchone()
            return res
        
    def add_action(self, user_id, action):
        with self.connection:
            res= self.cursor.execute("INSERT INTO actions (user_id, action, date) VALUES (?, ?, ?)", (user_id, action, dt.today(),))
            return res
        
    def inf_about_action(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT action FROM actions WHERE user_id= ?", (user_id, )).fetchall()
            return res
        
    def user_info(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT * FROM users_info WHERE user_id= ?", (user_id, )).fetchone()
            return res
        
    def add_user(self, user_id):
        with self.connection:
            res= self.cursor.execute("INSERT INTO users_info (user_id) VALUES (?)", (user_id,)).fetchone()
            return res
        
    def last_actions(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT DISTINCT action FROM actions WHERE user_id= ? and date >= ?", (user_id, dt.today()- timedelta(weeks=15),)).fetchall()
            return res
    
    def skip_user(self, user_id, sk=True):
        with self.connection:
            if sk is True:
                res= self.cursor.execute("UPDATE users_info SET skip= skip+1 WHERE user_id = ?", (user_id,))
            else:
                res= self.cursor.execute("UPDATE users_info SET skip= 0 WHERE user_id = ?", (user_id,))
            return res
        
    def add_focus(self, user_id, action, hour, point, date, category, duration =None):
        with self.connection:
            res= self.cursor.execute("INSERT INTO logs (user_id, action, hour, point, date, category, duration) VALUES (?,?,?,?,?,?,?)", (user_id, action, hour, point, date, category, duration,)) 
            return res
        
    def del_focus(self, user_id, action, date, category):
        with self.connection:
            res= self.cursor.execute("DELETE FROM logs WHERE user_id= ? and action = ? and date= ? and category= ?", (user_id, action, date, category,)) 
            return res
        
    def user_info_id(self):
        with self.connection:
            res= self.cursor.execute("SELECT user_id FROM users_info").fetchone()
            return res
        
    def get_points_atweek(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT SUM(point) FROM logs WHERE user_id= ? and (date >= ? and date < ?)", (user_id, (dt.today()- timedelta(days=7)), dt.today())).fetchone()
            return res
        
    def get_friends(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT friends FROM users_info WHERE user_id= ?", (user_id, )).fetchone()
            return res
        
    def find_id(self, user_name):
        with self.connection:
            res= self.cursor.execute("SELECT user_id FROM users_info WHERE user_name= ?", (user_name, )).fetchone()
            return res
        
    def get_short_stat(self, user_id, first_date, second_date):
        with self.connection:
            res= self.cursor.execute("SELECT SUM(hour), SUM(point) FROM logs WHERE user_id=? and (date >= ? and date < ?)", (user_id, first_date, second_date, )).fetchone()
            return res
        
    def get_user_name(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT user_name FROM users_info WHERE user_id= ?", (user_id, )).fetchone()
            return res
        
    def stat_short_today(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT `hour`, `point` FROM logs WHERE user_id= ? and `date` = ?", (user_id, dt.today(), )).fetchone()
            return res