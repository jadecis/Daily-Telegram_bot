import sqlite3
from datetime import timedelta, datetime
from datetime import date as dt       
        
class Database():
    
    def __init__(self, db_file):
        self.connection= sqlite3.connect(db_file)
        self.cursor= self.connection.cursor()
    
    def user_info(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?",(user_id, )).fetchone()
            if bool(result):
                return result
            else:
                return bool(result)
        
    def add_user(self, user_id, user_name):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name,))
    
    def up_name(self, user_id, user_name):
        with self.connection:
            self.cursor.execute("UPDATE users_info SET user_name= ? WHERE user_id = ?", (user_name, user_id,))
    
    def get_friends(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT friend_id FROM friends WHERE user_id= ?", (user_id, )).fetchall()
            if bool(len(res)) is False:
                return False
            else:
                return res
            
    def find_id(self, user_name):
        with self.connection:
            res= self.cursor.execute("SELECT user_id FROM users WHERE user_name = ?", (user_name, )).fetchone()
            if bool(res) is False:
                return False
            else:
                return res
            
    def add_friend(self, user_id, friend_id):
        with self.connection:
            try:
                self.cursor.execute("INSERT INTO friends (user_id, friend_id) VALUES (?, ?)", (user_id, friend_id, ))
                self.cursor.execute("INSERT INTO friends (friend_id, user_id) VALUES (?, ?)", (user_id, friend_id, ))
            except Exception as ex:
                print(ex)
                return False
    
    def del_friend(self, user_id, friend_id):
        with self.connection:   
            self.cursor.execute("DELETE FROM friends WHERE user_id = ? and friend_id= ?", (user_id, friend_id, ))
            self.cursor.execute("DELETE FROM friends WHERE user_id = ? and friend_id= ?", (friend_id, user_id,))
    
    def can_add_friend(self, user_id, friend_id):
        with self.connection:
            res= self.cursor.execute("SELECT id FROM friends WHERE friend_id= ? and user_id= ?", (friend_id, user_id,)).fetchone()
            if bool(res) is False:
                return True
            else:
                return False
            
    def add_focus(self, user_id, action, category, hour, point, date, duration=None):
        with self.connection:
            self.cursor.execute("INSERT INTO logs (user_id, action, category, hour, point, date, duration) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (user_id, action, category, hour, point, date, duration, ))
            
            return self.cursor.execute("SELECT max(id) FROM logs WHERE user_id= ?",
                                       (user_id,) ).fetchone()[0]
            
    def get_week(self):
        with self.connection:
            return  self.cursor.execute("SELECT id FROM logs WHERE date < ?", (dt.today(), )).fetchall()
        
    def count_logs(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(id) FROM logs WHERE user_id= ?", (user_id, )).fetchone()[0]
        
    def usefulles_user(self, user_id):
        with self.connection:
            category= self.cursor.execute("SELECT COUNT(id) FROM logs WHERE user_id= ? and category != ?", (user_id, "")).fetchone()[0]
            return bool(category)
        
    def skip_info(self, user_id):
        with self.connection:
            skip= self.cursor.execute("SELECT skip FROM users WHERE user_id= ?", (user_id, )).fetchone()[0]
            return skip
        
    def skip_user(self, user_id, sk=True):
        with self.connection:
            if sk is True:
                res= self.cursor.execute("UPDATE users SET skip= skip+1 WHERE user_id = ?", (user_id,))
            else:
                res= self.cursor.execute("UPDATE users SET skip= 0 WHERE user_id = ?", (user_id,))
            return res
        
    def del_logByKey(self, id):
        with self.connection:
            res= self.cursor.execute("SELECT * FROM logs WHERE id = ?", (id, )).fetchone()
            self.cursor.execute("DELETE FROM logs WHERE id = ?", (id, ))
            return res
        
    def last_actions(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT DISTINCT action FROM logs WHERE user_id= ? ORDER BY id DESC", (user_id, )).fetchmany(10)
        
    def stat_by_interval(self, user_id, first_date, second_date):
        with self.connection:
            res= self.cursor.execute("SELECT `action`, `hour`, `point`, id FROM `logs` WHERE `user_id` = ? and (`date` >= ? and `date` <= ?)",(user_id, first_date, second_date,) ).fetchall()
            return res
        
    def stat_today(self, user_id, date=dt.today()):
        with self.connection:
            return self.cursor.execute("SELECT `action`, `hour`, `point`, `category`, `duration` FROM logs WHERE user_id= ? and date = ?", (user_id, date, )).fetchall()

    def first_log(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT MIN(`date`) FROM logs WHERE user_id= ?", (user_id, )).fetchone()
        
    def stat_short_today(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT SUM(hour), SUM(point) FROM logs WHERE user_id= ? and `date` = ?", (user_id, dt.today(), )).fetchone()
            
    def get_short_stat(self, user_id, first_date, second_date):
        with self.connection:
            return self.cursor.execute("SELECT SUM(hour), SUM(point) FROM logs WHERE user_id=? and (date >= ? and date <= ?)", (user_id, first_date, second_date, )).fetchone()
        
    def user_info_id(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users").fetchall()
            
    def get_points_atweek(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT SUM(point) FROM logs WHERE user_id= ? and (date >= ? and date < ?)", (user_id, (dt.today()- timedelta(days=7)), dt.today())).fetchone()
        
    def shoke_user(self, user_id, sk=True):
        with self.connection:
            if sk is True:
                res= self.cursor.execute("UPDATE users SET shoke_mode= shoke_mode+1 WHERE user_id = ?", (user_id,))
            else:
                res= self.cursor.execute("UPDATE users SET shoke_mode= 0 WHERE user_id = ?", (user_id,))
            return res