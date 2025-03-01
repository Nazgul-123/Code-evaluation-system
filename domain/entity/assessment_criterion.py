import aiosqlite
import asyncio
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
# Получаем значение переменной окружения
DB_PATH = os.getenv("DB_PATH")

class AssessmentCriterion:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    async def create_table(self):
        """Создает таблицу для критериев оценивания, если она не существует."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS assessment_criteria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repository_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    FOREIGN KEY (repository_id) REFERENCES repository_settings(id)
                )
            ''')
            await db.commit()

    async def add_criterion(self, repository_id: int, content: str):
        """Добавляет новый критерий оценивания в базу данных."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO assessment_criteria (repository_id, content)
                VALUES (?, ?)
            ''', (repository_id, content))
            await db.commit()

    async def get_criterion(self, criterion_id: int):
        """Получает критерий оценивания по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM assessment_criteria WHERE id = ?', (criterion_id,)) as cursor:
                return await cursor.fetchone()

    async def update_criterion(self, criterion_id: int, repository_id: int, content: str):
        """Обновляет существующий критерий оценивания."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                UPDATE assessment_criteria
                SET repository_id = ?, content = ?
                WHERE id = ?
            ''', (repository_id, content, criterion_id))
            await db.commit()

    async def delete_criterion(self, criterion_id: int):
        """Удаляет критерий оценивания по его ID."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM assessment_criteria WHERE id = ?', (criterion_id,))
            await db.commit()

    async def list_criteria(self):
        """Возвращает список всех критериев оценивания."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM assessment_criteria') as cursor:
                return await cursor.fetchall()

    async def drop_table(self):
        """Удаляет таблицу критериев оценивания."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DROP TABLE IF EXISTS assessment_criteria")
            await db.commit()


# Пример использования
async def main():
    criterion_db = AssessmentCriterion()
    # Создание таблицы
    await criterion_db.create_table()
    print("Создали таблицу AssessmentCriterion")

    # Добавление критерия
    await criterion_db.add_criterion(repository_id=1, content="Код должен компилироваться без ошибок.")
    print("Добавили критерий")

    # Получение критерия
    criterion = await criterion_db.get_criterion(1)
    print("Полученный критерий:", criterion)

    # Обновление критерия
    await criterion_db.update_criterion(criterion_id=1, repository_id=1,
                                        content="Код должен компилироваться и выполняться корректно.")
    updated_criterion = await criterion_db.get_criterion(1)
    print("Обновленный критерий:", updated_criterion)

    # Список критериев
    all_criteria = await criterion_db.list_criteria()
    print("Все критерии:", all_criteria)

    # Удаление критерия
    await criterion_db.delete_criterion(1)
    print("Удалили критерий")

    # Список критериев
    all_criteria = await criterion_db.list_criteria()
    print("Все критерии:", all_criteria)

    # Удаление таблицы
    await criterion_db.drop_table()
    print("Удалили таблицу AssessmentCriterion")

if __name__ == "__main__":
    asyncio.run(main())
