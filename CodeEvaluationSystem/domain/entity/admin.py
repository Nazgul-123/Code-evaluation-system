import sqlite3
from config import DB_PATH, USERNAME, PASSWORD

class Administrator:
    def __init__(self, db_name=DB_PATH):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()
        self.username = USERNAME
        self.password = PASSWORD

    def create_table(self):
        """Создает таблицу для администратора, если она не существует."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS administrator (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.connection.commit()