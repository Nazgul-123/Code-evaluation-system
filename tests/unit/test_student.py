import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
import pytest_asyncio
from domain.entity.student import Student  # Импортируем класс Student
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
# Получаем значение переменной окружения
DB_PATH = os.getenv("DB_PATH")

@pytest_asyncio.fixture
async def student_db():
    """Фикстура для создания и очистки базы данных перед каждым тестом."""
    db = Student(DB_PATH)
    await db.create_student_table()  # Создаем таблицу перед тестом
    try:
        yield db  # Возвращаем объект базы данных для теста
    finally:
        await db.drop_student_table()  # Удаляем таблицу после теста

@pytest.mark.asyncio
async def test_create_student(student_db):
    """Тест создания студента."""
    await student_db.create_student(
        full_name="Иванов Иван",
        group_number="Группа 101",
        github_username="ivanov",
        email="ivanov@example.com"
    )
    student = await student_db.read_student(1)
    assert student is not None
    assert student[1] == "Иванов Иван"
    assert student[2] == "Группа 101"
    assert student[3] == "ivanov"
    assert student[4] == "ivanov@example.com"

@pytest.mark.asyncio
async def test_read_student(student_db):
    """Тест чтения студента."""
    await student_db.create_student(
        full_name="Сидоров Сидор",
        group_number="Группа 102",
        github_username="sidorov",
        email="sidorov@example.com"
    )
    student = await student_db.read_student(1)
    assert student is not None
    assert student[1] == "Сидоров Сидор"
    assert student[2] == "Группа 102"
    assert student[3] == "sidorov"
    assert student[4] == "sidorov@example.com"

@pytest.mark.asyncio
async def test_update_student(student_db):
    """Тест обновления студента."""
    await student_db.create_student(
        full_name="Петров Петр",
        group_number="Группа 103",
        github_username="petrov",
        email="petrov@example.com"
    )
    await student_db.update_student(
        student_id=1,
        full_name="Петр Петров",
        group_number="Группа 104",
        github_username="petr",
        email="petr@example.com"
    )
    student = await student_db.read_student(1)
    assert student is not None
    assert student[1] == "Петр Петров"
    assert student[2] == "Группа 104"
    assert student[3] == "petr"
    assert student[4] == "petr@example.com"

@pytest.mark.asyncio
async def test_delete_student(student_db):
    """Тест удаления студента."""
    await student_db.create_student(
        full_name="Кузнецов Николай",
        group_number="Группа 105",
        github_username="kuz",
        email="kuz@example.com"
    )
    await student_db.delete_student(1)
    student = await student_db.read_student(1)
    assert student is None

@pytest.mark.asyncio
async def test_list_students(student_db):
    """Тест получения списка студентов."""
    await student_db.create_student(
        full_name="Студент 1",
        group_number="Группа 101",
        github_username="student1",
        email="student1@example.com"
    )
    await student_db.create_student(
        full_name="Студент 2",
        group_number="Группа 102",
        github_username="student2",
        email="student2@example.com"
    )
    students = await student_db.list_students()
    assert len(students) == 2
    assert students[0][1] == "Студент 1"
    assert students[0][2] == "Группа 101"
    assert students[0][3] == "student1"
    assert students[0][4] == "student1@example.com"
    assert students[1][1] == "Студент 2"
    assert students[1][2] == "Группа 102"
    assert students[1][3] == "student2"
    assert students[1][4] == "student2@example.com"