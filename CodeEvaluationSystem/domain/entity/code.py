import sqlite3
from config import DB_PATH

class Code:
    def __init__(self, db_name=DB_PATH):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_code_table()

    def create_code_table(self):
        """Создает таблицу кодов, если она не существует."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                lab_number INTEGER NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
            )
        ''')
        self.connection.commit()

    def create_code(self, student_id: int, lab_number: int, content: str):
        """Создает новый код в базе данных."""
        self.cursor.execute('''
            INSERT INTO codes (student_id, lab_number, content)
            VALUES (?, ?, ?)
        ''', (student_id, lab_number, content))
        self.connection.commit()

    def read_code(self, code_id: int):
        """Читает данные кода по его ID."""
        self.cursor.execute('''
            SELECT * FROM codes WHERE id = ?
        ''', (code_id,))
        return self.cursor.fetchone()

    def update_code(self, code_id: int, student_id: int, lab_number: int, content: str):
        """Обновляет данные кода."""
        self.cursor.execute('''
            UPDATE codes
            SET student_id = ?, lab_number = ?, content = ?
            WHERE id = ?
        ''', (student_id, lab_number, content, code_id))
        self.connection.commit()

    def delete_code(self, code_id: int):
        """Удаляет код по его ID."""
        self.cursor.execute('''
            DELETE FROM codes WHERE id = ?
        ''', (code_id,))
        self.connection.commit()

    def list_codes(self):
        """Возвращает список всех кодов."""
        self.cursor.execute('SELECT * FROM codes')
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()


# Пример использования
if __name__ == "__main__":
    code_db = Code()

    # Создание кода
    code_db.create_code(1, 1, "print('Hello, World!')")

    # Чтение кода
    code = code_db.read_code(1)
    print("Код:", code)

    # Список кодов
    all_codes = code_db.list_codes()
    print("Все коды:", all_codes)

    # Закрытие базы данных
    code_db.close()
