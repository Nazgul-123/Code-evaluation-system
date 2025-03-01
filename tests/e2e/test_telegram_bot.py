import sys
import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from bot.main import evaluate_code, handle_code_submission, user_codes

@pytest.mark.asyncio
@patch('main.evaluate_lab_work_with_static_analyzer', new_callable=AsyncMock)
@patch('main.evaluate_lab_work_with_LLM', new_callable=AsyncMock)
@patch('main.ReportGenerator.generate_report', new_callable=AsyncMock)
@patch('main.bot', new_callable=MagicMock)
async def test_evaluate_code(mock_bot, mock_generate_report, mock_evaluate_llm, mock_evaluate_static):
    """Тест асинхронной функции оценки кода"""

    user_id = 12345
    user_codes[user_id] = "print('Hello World')"

    # Настройка заглушек
    mock_evaluate_static.return_value = "Статический анализ: все хорошо."
    mock_evaluate_llm.return_value = "LLM оценка: отлично."
    mock_generate_report.return_value = "Ваш отчет: все прошло успешно."

    # Создание объекта сообщения
    message = MagicMock()
    message.from_user.id = user_id
    message.chat.id = 67890
    message.message_id = 1

    # Настройка message.answer как асинхронного метода
    message.answer = AsyncMock()

    # Используем AsyncMock для асинхронного метода reply_to
    mock_bot.reply_to = AsyncMock()

    # Вызываем функцию
    await evaluate_code(message)

    # Проверяем, что методы были вызваны
    mock_evaluate_static.assert_called_once_with(1, "print('Hello World')")
    mock_evaluate_llm.assert_called_once_with(1, "print('Hello World')", "Критерии оценки лабораторной работы:")
    mock_generate_report.assert_called_once_with(
        student_id=str(user_id),
        LLMAssessment="LLM оценка: отлично.",
        staticAnalyserAssessment="Статический анализ: все хорошо."
    )
    message.answer.assert_called_once_with("Ваш отчет: все прошло успешно.")


@pytest.mark.asyncio
async def test_handle_code_submission():
    """Тест сохранения кода пользователя"""

    user_id = 12345
    message = MagicMock()
    message.from_user.id = user_id
    message.text = "print('Hello World')"
    message.chat.id = 67890

    # Настройка message.answer как асинхронного метода
    message.answer = AsyncMock()

    # Используем AsyncMock для асинхронного метода reply_to
    mock_bot = MagicMock()
    mock_bot.reply_to = AsyncMock()

    # Заменяем bot на mock_bot
    with patch('main.bot', mock_bot):
        await handle_code_submission(message)

    # Проверяем, что код был сохранен
    assert user_id in user_codes
    assert user_codes[user_id] == "print('Hello World')"

    # Проверяем, что message.answer был вызван
    message.answer.assert_called_once_with("Ваш код успешно загружен! Чтобы получить оценку, введите /evaluate.")