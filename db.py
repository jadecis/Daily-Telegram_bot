import sqlite3
from datetime import datetime, timedelta
from datetime import date as dt

class Database():
    def __init__(self, db_file):
        self.connection= sqlite3.connect(db_file)
        self.cursor= self.connection.cursor()
        
    def stat_by_interval(self, user_id, first_date, second_date):
        with self.connection:
            res= self.cursor.execute("SELECT `action`, `hour`, `point` FROM `logs` WHERE `user_id` = ? and (`date` >= ? and `date` < ?)",(user_id, first_date, second_date,) ).fetchall()
            return res
        
    def stat_today(self, user_id, date):
        with self.connection:
            res= self.cursor.execute("SELECT `action`, `hour`, `point`, `category`, `duration` FROM logs WHERE user_id= ? and `date` = ?", (user_id, date, )).fetchall()
            return res
        
    def first_log(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT MIN(`date`) FROM logs WHERE user_id= ?", (user_id, )).fetchone()
            return res
          
    def user_info(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT * FROM users_info WHERE user_id= ?", (user_id, )).fetchone()
            return res
        
    def add_user(self, user_id, user_name):
        with self.connection:
            res= self.cursor.execute("INSERT INTO users_info (user_id, user_name) VALUES (?, ?)", (user_id,user_name,)).fetchone()
            return res
        
    def last_actions(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT DISTINCT action FROM logs WHERE user_id= ? and date >= ?", (user_id, dt.today()- timedelta(weeks=15),)).fetchall()
            return res
    
    def skip_user(self, user_id, sk=True):
        with self.connection:
            if sk is True:
                res= self.cursor.execute("UPDATE users_info SET skip= skip+1 WHERE user_id = ?", (user_id,))
            else:
                res= self.cursor.execute("UPDATE users_info SET skip= 0 WHERE user_id = ?", (user_id,))
            return res
        
    def add_focus(self, user_id, action, hour, point, date, category, key, duration =None):
        with self.connection:
            res= self.cursor.execute("INSERT INTO logs (user_id, action, hour, point, date, category, key, duration) VALUES (?,?,?,?,?,?,?,?)", (user_id, action, hour, point, date, category, key, duration,)) 
            return res
        
    def del_focus(self, user_id, key):
        with self.connection:
            res= self.cursor.execute("DELETE FROM logs WHERE user_id= ? and key = ? ", (user_id, key,)) 
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
            res= self.cursor.execute("SELECT SUM(hour), SUM(point) FROM logs WHERE user_id=? and (date >= ? and date <= ?)", (user_id, first_date, second_date, )).fetchone()
            return res
        
    def get_user_name(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT user_name FROM users_info WHERE user_id= ?", (user_id, )).fetchone()
            return res
        
    def stat_short_today(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT SUM(hour), SUM(point) FROM logs WHERE user_id= ? and `date` = ?", (user_id, dt.today(), )).fetchone()
            return res
    
    def add_friend(self, user_id, friend_id):
        with self.connection:
            res= self.cursor.execute("UPDATE users_info SET friends=?  WHERE user_id = ?", (friend_id, user_id,))
            return res
        
    def get_user_shoke(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT shoke_mode FROM users_info WHERE user_id= ?", (user_id, )).fetchone()
            return res
        
    def shoke_user(self, user_id, sk=True):
        with self.connection:
            if sk is True:
                res= self.cursor.execute("UPDATE users_info SET shoke_mode= shoke_mode+1 WHERE user_id = ?", (user_id,))
            else:
                res= self.cursor.execute("UPDATE users_info SET shoke_mode= 0 WHERE user_id = ?", (user_id,))
            return res
        
    def up_name(self, user_id, user_name):
        with self.connection:
            res= self.cursor.execute("UPDATE users_info SET user_name= ? WHERE user_id = ?", (user_name, user_id,))
            return res
        
    def get_user_cat(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT category FROM logs WHERE user_id= ?", (user_id, )).fetchall()
            return res
        
    def get_count_logs(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT COUNT(action) FROM logs WHERE user_id= ?", (user_id, )).fetchone()
            return res
        
    def get_stat_by_key(self, user_id, key):
        with self.connection:
            res= self.cursor.execute("SELECT * FROM logs WHERE user_id= ? and key= ?", (user_id, key, )).fetchone()
            return res