import aiosqlite
import asyncio
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
# Получаем значение переменной окружения
DB_PATH = os.getenv("DB_PATH")

class Report:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    async def create_report_table(self):
        """Создает таблицу отчетов, если она не существует."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_id INTEGER NOT NULL,
                    feedback TEXT NOT NULL,
                    FOREIGN KEY (code_id) REFERENCES codes (id) ON DELETE CASCADE
                )
            ''')
            await db.commit()

    async def create_report(self, code_id: int, feedback: str):
        """Создает новый отчет в базе данных."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO reports (code_id, feedback)
                VALUES (?, ?)
            ''', (code_id, feedback))
            await db.commit()

    async def read_report(self, report_id: int):
        """Читает данные отчета по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM reports WHERE report_id = ?', (report_id,)) as cursor:
                return await cursor.fetchone()

    async def update_report(self, report_id: int, code_id: int, feedback: str):
        """Обновляет данные отчета."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                UPDATE reports
                SET code_id = ?, feedback = ?
                WHERE report_id = ?
            ''', (code_id, feedback, report_id))
            await db.commit()

    async def delete_report(self, report_id: int):
        """Удаляет отчет по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM reports WHERE report_id = ?', (report_id,))
            await db.commit()

    async def list_reports(self):
        """Возвращает список всех отчетов."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM reports') as cursor:
                return await cursor.fetchall()

    async def drop_report_table(self):
        """Удаляет таблицу отчетов."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DROP TABLE IF EXISTS reports")
            await db.commit()

# Пример использования
async def main():
    report_db = Report()

    # Создание таблицы для отчетов
    await report_db.create_report_table()
    print("Создали таблицу Report")

    # Пример создания отчета
    await report_db.create_report(1, "Отличная работа!")
    print("Добавили отчет")

    # Чтение отчета
    report = await report_db.read_report(1)
    print("Отчет:", report)

    # Обновление отчета
    await report_db.update_report(1, 1, "Хорошая работа, но можно лучше!")
    report = await report_db.read_report(1)
    print("Обновленный отчет:", report)

    # Список отчетов
    all_reports = await report_db.list_reports()
    print("Все отчеты:", all_reports)

    # Удаление отчета
    await report_db.delete_report(1)
    report = await report_db.read_report(1)
    print("Пытаемся получить удаленный отчет:", report)

    # Удаление таблицы
    await report_db.drop_report_table()
    print("Удалили таблицу Report")

if __name__ == "__main__":
    asyncio.run(main())