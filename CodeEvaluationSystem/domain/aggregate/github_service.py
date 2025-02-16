import requests
import os
from config import GITHUB_TOKEN

REPO_OWNER = 'Nazgul-123'
REPO_NAME = 'CSharp-LabWorks-HSE-Perm'

# Заголовки для авторизации
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

# Получаем список форков
forks_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/forks'

def get_forks() -> list:
    """
    Получает список форков репозитория с GitHub.
    :return: Список форков или None в случае ошибки.
    """

    try:
        # Выполняем GET-запрос
        response = requests.get(forks_url, headers=headers)

        # Проверяем статус ответа
        if response.status_code == 200:
            forks = response.json()
            print(f"Успешно получено {len(forks)} форков.")
            return forks
        else:
            print(f'Ошибка при получении форков: {response.status_code} - {response.text}')
            return None

    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return None


def clone_forks(forks: list) -> None:
    """
    Клонирует форки репозитория в локальную файловую систему.

    :param forks: Список форков.
    """
    if not forks:
        print("Нет форков для клонирования.")
        return

    for fork in forks:
        fork_owner = fork['owner']['login']
        fork_repo_name = fork['name']
        clone_url = fork['clone_url']

        print(f'Клонирование форка: {fork_owner}/{fork_repo_name}')
        os.system(f'git clone {clone_url} {fork_repo_name}')


def get_student_work(work_codes: list) -> None:
    """
    Отправляет коды студентов загруженные из GitHub в виде списка текстов.

    :param work_codes: Список кодов работ студентов.
    """
    work_codes = ["код работы 1", "код работы 2", "код работы 3"] #перевод работ в строковый формат
    return work_codes
