import aiosqlite
import asyncio
from config import DB_PATH

class Teacher:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    async def create_teacher_table(self):
        """Создает таблицу преподавателей, если она не существует."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            ''')
            await db.commit()

    async def create_teacher(self, full_name: str, email: str):
        """Создает нового преподавателя в базе данных."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO teachers (full_name, email)
                VALUES (?, ?)
            ''', (full_name, email))
            await db.commit()

    async def read_teacher(self, teacher_id: int):
        """Читает данные преподавателя по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM teachers WHERE id = ?', (teacher_id,)) as cursor:
                return await cursor.fetchone()

    async def update_teacher(self, teacher_id: int, full_name: str, email: str):
        """Обновляет данные преподавателя."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                UPDATE teachers
                SET full_name = ?, email = ?
                WHERE id = ?
            ''', (full_name, email, teacher_id))
            await db.commit()

    async def delete_teacher(self, teacher_id: int):
        """Удаляет преподавателя по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM teachers WHERE id = ?', (teacher_id,))
            await db.commit()

    async def list_teachers(self):
        """Возвращает список всех преподавателей."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM teachers') as cursor:
                return await cursor.fetchall()

    async def drop_teacher_table(self):
        """Удаляет таблицу преподавателей."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DROP TABLE IF EXISTS teachers")
            await db.commit()

# Пример использования
async def main():
    teacher_db = Teacher()

    # Создание таблицы преподавателей
    await teacher_db.create_teacher_table()
    print("Создали таблицу Teacher")

    # Пример создания преподавателя
    await teacher_db.create_teacher("Петров Петр Петрович", "petrov@example.com")
    print("Добавили преподавателя")

    # Чтение преподавателя
    teacher = await teacher_db.read_teacher(1)
    print("Преподаватель:", teacher)

    # Обновление преподавателя
    await teacher_db.update_teacher(1, "Петров Петр Петрович", "petrov_updated@example.com")
    teacher = await teacher_db.read_teacher(1)
    print("Обновленный преподаватель:", teacher)

    # Список преподавателей
    all_teachers = await teacher_db.list_teachers()
    print("Все преподаватели:", all_teachers)

    # Удаление преподавателя
    await teacher_db.delete_teacher(1)
    teacher = await teacher_db.read_teacher(1)
    print("Пытаемся получить удаленного преподавателя:", teacher)

    # Удаление таблицы
    await teacher_db.drop_teacher_table()
    print("Удалили таблицу Teacher")

if __name__ == "__main__":
    asyncio.run(main())