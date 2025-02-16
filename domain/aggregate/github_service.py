import os
import aiohttp
import asyncio
from git import Repo
from config import GITHUB_TOKEN

# Константы для GitHub репозитория
REPO_OWNER = 'Nazgul-123'
REPO_NAME = 'CSharp-LabWorks-HSE-Perm'

# Заголовки для авторизации
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

# URL для работы с API GitHub
FORKS_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/forks'


async def get_forks() -> list:
    """
    Получает список форков репозитория с GitHub асинхронно.

    :return: Список форков или пустой список, если произошла ошибка.
    """
    # Заглушка для списка форков
    mock_forks = [
        {"owner": {"login": "student1"}, "name": "repo1", "clone_url": "https://github.com/student1/repo1.git"},
        {"owner": {"login": "student2"}, "name": "repo2", "clone_url": "https://github.com/student2/repo2.git"}
    ]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FORKS_URL, headers=HEADERS) as response:
                if response.status == 200:
                    forks = await response.json()
                    print(f"Успешно получено {len(forks)} форков.")
                    return forks
                else:
                    print(f'Ошибка при получении форков: {response.status} - {await response.text()}')
                    return mock_forks  # Возвращаем заглушку в случае ошибки
                    #return []
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return mock_forks  # Возвращаем заглушку в случае ошибки
        #return []


async def clone_fork(fork: dict, target_directory: str) -> None:
    """
    Клонирует форк в указанную локальную директорию.

    :param fork: Словарь с информацией о форке.
    :param target_directory: Путь для сохранения клонированного репозитория.
    """
    try:
        fork_owner = fork.get('owner', {}).get('login', 'unknown')
        fork_repo_name = fork.get('name', 'unknown-repo')
        clone_url = fork.get('clone_url')

        if not clone_url:
            print(f"Не найден clone_url для форка {fork_owner}/{fork_repo_name}")
            return

        print(f'Клонирование форка: {fork_owner}/{fork_repo_name} в {target_directory}/{fork_repo_name}')
        repo_path = os.path.join(target_directory, fork_repo_name)

        # Используем GitPython для клонирования
        Repo.clone_from(clone_url, repo_path)
        print(f'Форк {fork_owner}/{fork_repo_name} успешно клонирован.')
    except Exception as e:
        print(f"Произошла ошибка при клонировании {fork.get('name')}: {e}")


async def clone_forks(forks: list, target_directory: str) -> None:
    """
    Асинхронно клонирует все форки репозитория.

    :param forks: Список форков.
    :param target_directory: Путь для сохранения всех репозиториев.
    """
    if not forks:
        print("Нет форков для клонирования.")
        return

    # Создаём папку для репозиториев, если её не существует
    os.makedirs(target_directory, exist_ok=True)

    # Асинхронно клонируем каждый форк
    tasks = [clone_fork(fork, target_directory) for fork in forks]
    await asyncio.gather(*tasks)
    print("Все форки успешно клонированы.")


async def get_student_work_by_username(username: str, target_directory: str) -> list[str]:
    """
    Возвращает работы студента в виде списка строк (сорцов) по имени пользователя на GitHub.

    :param username: Имя пользователя GitHub для поиска.
    :param target_directory: Локальная директория, где хранятся клонированные форки.
    :return: Список текстов файлов студентов.
    """
    student_repo_path = os.path.join(target_directory, username)
    if not os.path.exists(student_repo_path):
        print(f"Репозиторий студента {username} не найден в {target_directory}.")
        return []

    try:
        # Считываем все файлы в репозитории студента
        work_codes = []
        for root, _, files in os.walk(student_repo_path):
            for file in files:
                if file.endswith(('.cs', '.py', '.java')):  # Фильтр по расширениям
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        work_codes.append(f.read())
        print(f"Работы студента {username} успешно извлечены. Всего файлов: {len(work_codes)}.")
        return work_codes
    except Exception as e:
        print(f"Ошибка при чтении файлов студента {username}: {e}")
        return []


async def get_all_student_works(target_directory: str) -> dict:
    """
    Возвращает работы всех студентов (всех форков) в виде словаря.

    :param target_directory: Локальная директория, где хранятся клонированные форки.
    :return: Словарь {имя пользователя: список текстов файлов}.
    """
    try:
        all_works = {}
        for folder_name in os.listdir(target_directory):
            student_repo_path = os.path.join(target_directory, folder_name)
            if os.path.isdir(student_repo_path):
                all_works[folder_name] = await get_student_work_by_username(folder_name, target_directory)
        print(f"Работы всех студентов успешно извлечены. Всего студентов: {len(all_works)}.")
        return all_works
    except Exception as e:
        print(f"Ошибка при извлечении работ: {e}")
        return {}


async def main():
    """
    Основная функция для демонстрации работы системы.
    """
    target_directory = './cloned_repos'

    # Получаем список форков
    forks = await get_forks()

    # Клонируем форки
    await clone_forks(forks, target_directory)

    # Извлекаем работы конкретного студента
    student_username = 'example_student'
    student_work = await get_student_work_by_username(student_username, target_directory)
    print(f"Коды студента {student_username}: {student_work}")

    # Извлекаем работы всех студентов
    all_works = await get_all_student_works(target_directory)
    print(f"Все работы студентов: {all_works}")


if __name__ == '__main__':
    asyncio.run(main())
