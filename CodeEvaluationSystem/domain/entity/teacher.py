import sqlite3
from config import DB_PATH

class Teacher:
    def __init__(self, db_name=DB_PATH):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Создает таблицу преподавателей, если она не существует."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        self.connection.commit()

    def create_teacher(self, full_name: str, email: str):
        """Создает нового преподавателя в базе данных."""
        self.cursor.execute('''
            INSERT INTO teachers (full_name, email)
            VALUES (?, ?)
        ''', (full_name, email))
        self.connection.commit()

    def read_teacher(self, teacher_id: int):
        """Читает данные преподавателя по его ID."""
        self.cursor.execute('''
            SELECT * FROM teachers WHERE id = ?
        ''', (teacher_id,))
        return self.cursor.fetchone()

    def update_teacher(self, teacher_id: int, full_name: str, email: str):
        """Обновляет данные преподавателя."""
        self.cursor.execute('''
            UPDATE teachers
            SET full_name = ?, email = ?
            WHERE id = ?
        ''', (full_name, email, teacher_id))
        self.connection.commit()

    def delete_teacher(self, teacher_id: int):
        """Удаляет преподавателя по его ID."""
        self.cursor.execute('''
            DELETE FROM teachers WHERE id = ?
        ''', (teacher_id,))
        self.connection.commit()

    def list_teachers(self):
        """Возвращает список всех преподавателей."""
        self.cursor.execute('SELECT * FROM teachers')
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()


# Пример использования
if __name__ == "__main__":
    teacher_db = Teacher()

    # Создание преподавателя
    teacher_db.create_teacher("Петров Петр Петрович", "petrov@example.com")

    # Чтение преподавателя
    teacher = teacher_db.read_teacher(1)
    print("Преподаватель:", teacher)

    # Обновление преподавателя
    teacher_db.update_teacher(1, "Петров Петр Петрович", "petrov_updated@example.com")

    # Список преподавателей
    all_teachers = teacher_db.list_teachers()
    print("Все преподаватели:", all_teachers)

    # Удаление преподавателя
    teacher_db.delete_teacher(1)

    # Закрытие базы данных
    teacher_db.close()
