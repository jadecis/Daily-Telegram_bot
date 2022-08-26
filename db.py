import sqlite3

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
            res= self.cursor.execute("SELECT `action`, `hour`, `point`, `category`, `duration` FROM logs WHERE user_id= ? and `date` = ?", (user_id, date, )).fetchall()
            return res
        
    def first_log(self, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT MIN(`date`) FROM logs WHERE user_id= ?", (user_id, )).fetchone()
            return res