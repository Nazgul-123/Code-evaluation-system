import aiosqlite
import asyncio
from config import DB_PATH

class Student:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    async def create_student_table(self):
        """Создает таблицу студентов, если она не существует."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    group_number TEXT NOT NULL,
                    github_username TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            ''')
            await db.commit()

    async def create_student(self, full_name: str, group_number: str, github_username: str, email: str):
        """Создает нового студента в базе данных."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO students (full_name, group_number, github_username, email)
                VALUES (?, ?, ?, ?)
            ''', (full_name, group_number, github_username, email))
            await db.commit()

    async def read_student(self, student_id: int):
        """Читает данные студента по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM students WHERE id = ?', (student_id,)) as cursor:
                return await cursor.fetchone()

    async def update_student(self, student_id: int, full_name: str, group_number: str, github_username: str, email: str):
        """Обновляет данные студента."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                UPDATE students
                SET full_name = ?, group_number = ?, github_username = ?, email = ?
                WHERE id = ?
            ''', (full_name, group_number, github_username, email, student_id))
            await db.commit()

    async def delete_student(self, student_id: int):
        """Удаляет студента по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM students WHERE id = ?', (student_id,))
            await db.commit()

    async def list_students(self):
        """Возвращает список всех студентов."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM students') as cursor:
                return await cursor.fetchall()

    async def drop_student_table(self):
        """Удаляет таблицу студентов."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DROP TABLE IF EXISTS students")
            await db.commit()

# Пример использования
async def main():
    student_db = Student()

    # Создание таблицы студентов
    await student_db.create_student_table()
    print("Создали таблицу Student")

    # Пример создания студента
    await student_db.create_student("Иванов Иван Иванович", "Группа 101", "ivanov123", "ivanov@example.com")
    print("Добавили студента")

    # Чтение студента
    student = await student_db.read_student(1)
    print("Студент:", student)

    # Обновление студента
    await student_db.update_student(1, "Иванов Иван Иванович", "Группа 102", "ivanov_updated", "ivanov_updated@example.com")
    student = await student_db.read_student(1)
    print("Обновленный студент:", student)

    # Список студентов
    all_students = await student_db.list_students()
    print("Все студенты:", all_students)

    # Удаление студента
    await student_db.delete_student(1)
    student = await student_db.read_student(1)
    print("Пытаемся получить удаленного студента:", student)

    # Удаление таблицы
    await student_db.drop_student_table()
    print("Удалили таблицу Student")

if __name__ == "__main__":
    asyncio.run(main())