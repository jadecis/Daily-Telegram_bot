import sqlite3

class Databae():
    def __init__(self, db_file):
        self.connection= sqlite3.connect(db_file)
        self.cursor= self.connection.cursor()
        
    