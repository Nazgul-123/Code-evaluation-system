import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
import pytest_asyncio
from domain.entity.report import Report  # Импортируем класс Report
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
# Получаем значение переменной окружения
DB_PATH = os.getenv("DB_PATH")

@pytest_asyncio.fixture
async def report_db():
    """Фикстура для создания и очистки базы данных перед каждым тестом."""
    db = Report(DB_PATH)
    await db.create_report_table()  # Создаем таблицу перед тестом
    try:
        yield db  # Возвращаем объект базы данных для теста
    finally:
        await db.drop_report_table()  # Удаляем таблицу после теста

@pytest.mark.asyncio
async def test_create_report(report_db):
    """Тест создания отчета."""
    await report_db.create_report(
        code_id=1,
        feedback="Отличный код!"
    )
    report = await report_db.read_report(1)
    assert report is not None
    assert report[1] == 1  # code_id
    assert report[2] == "Отличный код!"  # feedback

@pytest.mark.asyncio
async def test_read_report(report_db):
    """Тест чтения отчета."""
    await report_db.create_report(
        code_id=2,
        feedback="Нужно доработать."
    )
    report = await report_db.read_report(1)
    assert report is not None
    assert report[1] == 2  # code_id
    assert report[2] == "Нужно доработать."  # feedback

@pytest.mark.asyncio
async def test_update_report(report_db):
    """Тест обновления отчета."""
    await report_db.create_report(
        code_id=3,
        feedback="Плохой код."
    )
    await report_db.update_report(
        report_id=1,
        code_id=3,
        feedback="Код улучшен."
    )
    report = await report_db.read_report(1)
    assert report is not None
    assert report[1] == 3  # code_id
    assert report[2] == "Код улучшен."  # feedback

@pytest.mark.asyncio
async def test_delete_report(report_db):
    """Тест удаления отчета."""
    await report_db.create_report(
        code_id=4,
        feedback="Отличная работа!"
    )
    await report_db.delete_report(1)
    report = await report_db.read_report(1)
    assert report is None

@pytest.mark.asyncio
async def test_list_reports(report_db):
    """Тест получения списка отчетов."""
    await report_db.create_report(
        code_id=5,
        feedback="Первый отчет."
    )
    await report_db.create_report(
        code_id=6,
        feedback="Второй отчет."
    )
    reports = await report_db.list_reports()
    assert len(reports) == 2
    assert reports[0][1] == 5  # code_id
    assert reports[0][2] == "Первый отчет."  # feedback
    assert reports[1][1] == 6  # code_id
    assert reports[1][2] == "Второй отчет."  # feedback