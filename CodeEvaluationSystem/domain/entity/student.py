import sqlite3
from config import DB_PATH

class Student:
    def __init__(self, db_name=DB_PATH):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Создает таблицу студентов, если она не существует."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                group_number TEXT NOT NULL,
                github_username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        self.connection.commit()

    def create_student(self, full_name: str, group_number: str, github_username: str, email: str):
        """Создает нового студента в базе данных."""
        self.cursor.execute('''
            INSERT INTO students (full_name, group_number, github_username, email)
            VALUES (?, ?, ?, ?)
        ''', (full_name, group_number, github_username, email))
        self.connection.commit()

    def read_student(self, student_id: int):
        """Читает данные студента по его ID."""
        self.cursor.execute('''
            SELECT * FROM students WHERE id = ?
        ''', (student_id,))
        return self.cursor.fetchone()

    def update_student(self, student_id: int, full_name: str, group_number: str, github_username: str, email: str):
        """Обновляет данные студента."""
        self.cursor.execute('''
            UPDATE students
            SET full_name = ?, group_number = ?, github_username = ?, email = ?
            WHERE id = ?
        ''', (full_name, group_number, github_username, email, student_id))
        self.connection.commit()

    def delete_student(self, student_id: int):
        """Удаляет студента по его ID."""
        self.cursor.execute('''
            DELETE FROM students WHERE id = ?
        ''', (student_id,))
        self.connection.commit()

    def list_students(self):
        """Возвращает список всех студентов."""
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()


# Пример использования
if __name__ == "__main__":
    student_db = Student()

    # Создание студента
    student_db.create_student("Иванов Иван Иванович", "Группа 101", "ivanov123", "ivanov@example.com")

    # Чтение студента
    student = student_db.read_student(1)
    print("Студент:", student)

    # Обновление студента
    student_db.update_student(1, "Иванов Иван Иванович", "Группа 102", "ivanov_updated", "ivanov_updated@example.com")

    # Список студентов
    all_students = student_db.list_students()
    print("Все студенты:", all_students)

    # Удаление студента
    student_db.delete_student(1)

    # Закрытие базы данных
    student_db.close()
