#здесь пока заглушки, работа бота проверялась вручную
import unittest
from unittest.mock import patch, MagicMock
from telebot import TeleBot
from main import bot, user_codes  # Импортируйте ваш бот и словарь user_codes


class TestTelegramBot(unittest.TestCase):

    @patch('main.evaluate_lab_work_with_static_analyzer')
    @patch('main.evaluate_lab_work_with_LLM')
    @patch('main.ReportGenerator.generate_report')
    def test_evaluate_code(self, mock_generate_report, mock_evaluate_llm, mock_evaluate_static):
        # Настройка заглушек
        user_id = 12345
        user_codes[user_id] = "print('Hello World')"

        mock_evaluate_static.return_value = "Статический анализ: все хорошо."
        mock_evaluate_llm.return_value = "LLM оценка: отлично."
        mock_generate_report.return_value = "Ваш отчет: все прошло успешно."

        # Создание объекта сообщения
        message = MagicMock()
        message.from_user.id = user_id
        message.chat.id = 67890  # Добавляем chat.id для корректной работы bot.reply_to

        # Вызов функции оценки
        from main import evaluate_code  # Импортируем функцию evaluate_code
        evaluate_code(message)

        # Проверка, что функции были вызваны
        mock_evaluate_static.assert_called_once_with(1, "print('Hello World')")
        mock_evaluate_llm.assert_called_once_with(1, "print('Hello World')", "Критерии оценки лабораторной работы:")
        mock_generate_report.assert_called_once_with(
            student_id=user_id,
            LLMAssessment="LLM оценка: отлично.",
            staticAnalyserAssessment="Статический анализ: все хорошо."
        )

    @patch('main.bot.reply_to')
    def test_handle_code_submission(self, mock_reply_to):
        user_id = 12345
        message = MagicMock()
        message.from_user.id = user_id
        message.text = "print('Hello World')"
        message.chat.id = 67890  # Добавляем chat.id для корректной работы bot.reply_to

        # Вызов функции обработки загрузки кода
        from main import handle_code_submission  # Импортируем функцию handle_code_submission
        handle_code_submission(message)

        # Проверка, что код был сохранен и ответ пользователю был отправлен
        self.assertIn(user_id, user_codes)
        self.assertEqual(user_codes[user_id], "print('Hello World')")
        mock_reply_to.assert_called_once_with(message,
                                              "Ваш код успешно загружен! Чтобы получить оценку, введите /evaluate.")


if __name__ == '__main__':
    unittest.main()