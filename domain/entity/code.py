import aiosqlite
import asyncio
from config import DB_PATH

class Code:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    async def create_code_table(self):
        """Создает таблицу кодов, если она не существует."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
            CREATE TABLE IF NOT EXISTS codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                lab_number INTEGER NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
                )
            ''')
            await db.commit()

    async def create_code(self, student_id: int, lab_number: int, content: str):
        """Создает новый код в базе данных."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
            INSERT INTO codes (student_id, lab_number, content)
            VALUES (?, ?, ?)
            ''', (student_id, lab_number, content))
            await db.commit()

    async def read_code(self, code_id: int):
        """Читает данные кода по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('''SELECT * FROM codes WHERE id = ?''', (code_id,)) as cursor:
                return await cursor.fetchone()

    async def update_code(self, code_id: int, student_id: int, lab_number: int, content: str):
        """Обновляет данные кода."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
            UPDATE codes
            SET student_id = ?, lab_number = ?, content = ?
            WHERE id = ?
            ''', (student_id, lab_number, content, code_id))
            await db.commit()

    async def delete_code(self, code_id: int):
        """Удаляет код по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
            DELETE FROM codes WHERE id = ?
            ''', (code_id,))
            await db.commit()

    async def list_codes(self):
        """Возвращает список всех кодов."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM codes') as cursor:
                return await cursor.fetchall()

    async def drop_code_table(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DROP TABLE IF EXISTS codes")
            await db.commit()

# Пример использования
async def main():
    code_db = Code()

    # Создание таблицы для кодов
    await code_db.create_code_table()
    print("Создаем таблицу Code")

    # Пример создания кода
    await code_db.create_code(1, 1, "print('Hello, World!')")

    # Пример чтения кода
    code = await code_db.read_code(1)
    print("Код: ", code)

    # Обновляем код
    await code_db.update_code(1, 2, 2, "print('Updated Hello World!')")
    code = await code_db.read_code(1)
    print("Обновленный код: ", code)

    # Пример получения всех кодов
    all_codes = await code_db.list_codes()
    print("Все коды: ", all_codes)

    # Удаляем код
    await code_db.delete_code(1)

    code = await code_db.read_code(1)
    print("Пытаемся получить удаленный код: ", code)

    await code_db.drop_code_table()
    print("Удаляем таблицу Code")

# Запуск основной асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())