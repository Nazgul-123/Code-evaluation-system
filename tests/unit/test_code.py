import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
import pytest_asyncio
from domain.entity.code import Code  # Импортируем класс Code
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
# Получаем значение переменной окружения
DB_PATH = os.getenv("DB_PATH")

@pytest_asyncio.fixture
async def code_db():
    """Фикстура для создания и очистки базы данных перед каждым тестом."""
    db = Code(DB_PATH)
    await db.create_code_table()  # Создаем таблицу перед тестом
    try:
        yield db  # Возвращаем объект базы данных для теста
    finally:
        await db.drop_code_table()  # Удаляем таблицу после теста

@pytest.mark.asyncio
async def test_create_code(code_db):
    """Тест создания кода."""
    await code_db.create_code(
        student_id=1,
        lab_number=1,
        content="print('Hello, World!')"
    )
    code = await code_db.read_code(1)
    assert code is not None
    assert code[1] == 1  # student_id
    assert code[2] == 1  # lab_number
    assert code[3] == "print('Hello, World!')"  # content

@pytest.mark.asyncio
async def test_read_code(code_db):
    """Тест чтения кода."""
    await code_db.create_code(
        student_id=2,
        lab_number=2,
        content="print('Goodbye, World!')"
    )
    code = await code_db.read_code(1)
    assert code is not None
    assert code[1] == 2  # student_id
    assert code[2] == 2  # lab_number
    assert code[3] == "print('Goodbye, World!')"  # content

@pytest.mark.asyncio
async def test_update_code(code_db):
    """Тест обновления кода."""
    await code_db.create_code(
        student_id=3,
        lab_number=3,
        content="print('Old Code')"
    )
    await code_db.update_code(
        code_id=1,
        student_id=3,
        lab_number=3,
        content="print('New Code')"
    )
    code = await code_db.read_code(1)
    assert code is not None
    assert code[1] == 3  # student_id
    assert code[2] == 3  # lab_number
    assert code[3] == "print('New Code')"  # content

@pytest.mark.asyncio
async def test_delete_code(code_db):
    """Тест удаления кода."""
    await code_db.create_code(
        student_id=4,
        lab_number=4,
        content="print('Delete Me')"
    )
    await code_db.delete_code(1)
    code = await code_db.read_code(1)
    assert code is None

@pytest.mark.asyncio
async def test_list_codes(code_db):
    """Тест получения списка кодов."""
    await code_db.create_code(
        student_id=5,
        lab_number=5,
        content="print('First Code')"
    )
    await code_db.create_code(
        student_id=6,
        lab_number=6,
        content="print('Second Code')"
    )
    codes = await code_db.list_codes()
    assert len(codes) == 2
    assert codes[0][1] == 5  # student_id
    assert codes[0][2] == 5  # lab_number
    assert codes[0][3] == "print('First Code')"  # content
    assert codes[1][1] == 6  # student_id
    assert codes[1][2] == 6  # lab_number
    assert codes[1][3] == "print('Second Code')"  # content