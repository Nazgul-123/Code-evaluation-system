import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
import pytest_asyncio
from domain.entity.assessment_criterion import AssessmentCriterion  # Импортируем класс AssessmentCriterion
from config import DB_PATH  # Импортируем конфигурационные данные

@pytest_asyncio.fixture
async def assessment_criterion_db():
    """Фикстура для создания и очистки базы данных перед каждым тестом."""
    db = AssessmentCriterion(DB_PATH)
    await db.create_table()  # Создаем таблицу перед тестом
    try:
        yield db  # Возвращаем объект базы данных для теста
    finally:
        await db.drop_table()  # Удаляем таблицу после теста

@pytest.mark.asyncio
async def test_add_criterion(assessment_criterion_db):
    """Тест добавления критерия оценивания."""
    await assessment_criterion_db.add_criterion(
        repository_id=1,
        content="Критерий 1"
    )
    criterion = await assessment_criterion_db.get_criterion(1)
    assert criterion is not None
    assert criterion[1] == 1  # repository_id
    assert criterion[2] == "Критерий 1"  # content

@pytest.mark.asyncio
async def test_get_criterion(assessment_criterion_db):
    """Тест получения критерия оценивания."""
    await assessment_criterion_db.add_criterion(
        repository_id=2,
        content="Критерий 2"
    )
    criterion = await assessment_criterion_db.get_criterion(1)
    assert criterion is not None
    assert criterion[1] == 2  # repository_id
    assert criterion[2] == "Критерий 2"  # content

@pytest.mark.asyncio
async def test_update_criterion(assessment_criterion_db):
    """Тест обновления критерия оценивания."""
    await assessment_criterion_db.add_criterion(
        repository_id=3,
        content="Старый критерий"
    )
    await assessment_criterion_db.update_criterion(
        criterion_id=1,
        repository_id=3,
        content="Новый критерий"
    )
    criterion = await assessment_criterion_db.get_criterion(1)
    assert criterion is not None
    assert criterion[1] == 3  # repository_id
    assert criterion[2] == "Новый критерий"  # content

@pytest.mark.asyncio
async def test_delete_criterion(assessment_criterion_db):
    """Тест удаления критерия оценивания."""
    await assessment_criterion_db.add_criterion(
        repository_id=4,
        content="Критерий для удаления"
    )
    await assessment_criterion_db.delete_criterion(1)
    criterion = await assessment_criterion_db.get_criterion(1)
    assert criterion is None

@pytest.mark.asyncio
async def test_list_criteria(assessment_criterion_db):
    """Тест получения списка критериев оценивания."""
    await assessment_criterion_db.add_criterion(
        repository_id=5,
        content="Критерий 1"
    )
    await assessment_criterion_db.add_criterion(
        repository_id=6,
        content="Критерий 2"
    )
    criteria = await assessment_criterion_db.list_criteria()
    assert len(criteria) == 2
    assert criteria[0][1] == 5  # repository_id
    assert criteria[0][2] == "Критерий 1"  # content
    assert criteria[1][1] == 6  # repository_id
    assert criteria[1][2] == "Критерий 2"  # content