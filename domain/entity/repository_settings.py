import aiosqlite
import asyncio
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
# Получаем значение переменной окружения
DB_PATH = os.getenv("DB_PATH")

class RepositorySettings:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    async def create_table(self):
        """Создает таблицу для хранения настроек репозитория, если она не существует."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS repository_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_url TEXT NOT NULL,
                    access_token TEXT NOT NULL,
                    github_owner TEXT NOT NULL,
                    github_repo_name TEXT NOT NULL,
                    discipline_name TEXT NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()

    async def set_repository(self, repo_url: str, access_token: str, github_owner: str, github_repo_name: str,
                             discipline_name: str):
        """Создает или обновляет запись о репозитории."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO repository_settings (repo_url, access_token, github_owner, github_repo_name, discipline_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (repo_url, access_token, github_owner, github_repo_name, discipline_name))
            await db.commit()

    async def get_repository(self):
        """Получает текущие настройки репозитория."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM repository_settings LIMIT 1') as cursor:
                return await cursor.fetchone()

    async def drop_repository_table(self):
        """Удаляет таблицу repository_settings, если она существует."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DROP TABLE IF EXISTS repository_settings')
            await db.commit()


# Пример использования
async def main():
    repo_db = RepositorySettings()

    # Создание таблицы
    await repo_db.create_table()
    print("Создали таблицу repository_settings")

    # Установка репозитория с указанием дисциплины
    await repo_db.set_repository(
        "https://github.com/org/repo",
        "ghp_exampleToken",
        "admin_user",
        "example-repo",
        "Программирование на C#"
    )
    print("Добавили данные о репозитории")

    # Получение данных
    repo = await repo_db.get_repository()
    print("Данные репозитория:", repo)

    # Удаление данных
    await repo_db.drop_repository_table()
    print("Удалили данные о репозитории")


if __name__ == "__main__":
    asyncio.run(main())
