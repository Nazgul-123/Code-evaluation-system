import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
import pytest_asyncio
import aiosqlite
from domain.entity.teacher import Teacher
from config import DB_PATH

@pytest_asyncio.fixture
async def teacher_db():
    db = Teacher(DB_PATH)
    await db.create_teacher_table()
    try:
        yield db  # Возвращаем объект базы данных для теста
    finally:
        await db.drop_teacher_table()  # Удаляем таблицу после теста

@pytest.mark.asyncio
async def test_create_teacher(teacher_db):
    await teacher_db.create_teacher("Иванов Иван", "ivanov@example.com")
    teacher = await teacher_db.read_teacher(1)
    assert teacher is not None
    assert teacher[1] == "Иванов Иван"
    assert teacher[2] == "ivanov@example.com"

@pytest.mark.asyncio
async def test_read_teacher(teacher_db):
    await teacher_db.create_teacher("Сидоров Сидор", "sidorov@example.com")
    teacher = await teacher_db.read_teacher(1)
    assert teacher is not None
    assert teacher[1] == "Сидоров Сидор"

@pytest.mark.asyncio
async def test_update_teacher(teacher_db):
    await teacher_db.create_teacher("Петров Петр", "petrov@example.com")
    await teacher_db.update_teacher(1, "Петр Петров", "petr@example.com")
    teacher = await teacher_db.read_teacher(1)
    assert teacher is not None
    assert teacher[1] == "Петр Петров"
    assert teacher[2] == "petr@example.com"

@pytest.mark.asyncio
async def test_delete_teacher(teacher_db):
    await teacher_db.create_teacher("Кузнецов Николай", "kuz@example.com")
    await teacher_db.delete_teacher(1)
    teacher = await teacher_db.read_teacher(1)
    assert teacher is None

@pytest.mark.asyncio
async def test_list_teachers(teacher_db):
    await teacher_db.create_teacher("Учитель 1", "teacher1@example.com")
    await teacher_db.create_teacher("Учитель 2", "teacher2@example.com")
    teachers = await teacher_db.list_teachers()
    assert len(teachers) == 2
    assert teachers[0][1] == "Учитель 1"
    assert teachers[1][1] == "Учитель 2"