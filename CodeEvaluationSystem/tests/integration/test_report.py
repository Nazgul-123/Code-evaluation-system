import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from domain.entity.report import Report  # Импортируем класс Report
from config import DB_PATH  # Импортируем конфигурационные данные


class TestReport(unittest.TestCase):

    @patch('sqlite3.connect')
    def setUp(self, mock_connect):
        """Настройка моков для каждого теста."""
        # Создаем мок для соединения с базой данных
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Создаем экземпляр класса Report
        self.report_db = Report()

    def test_create_report_table(self):
        """Тест создания таблицы reports."""
        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = '''
            CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_id INTEGER NOT NULL,
                feedback TEXT NOT NULL,
                FOREIGN KEY (code_id) REFERENCES codes (id) ON DELETE CASCADE
            )
        '''
        self.mock_cursor.execute.assert_called_once_with(expected_query)

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called_once()

    def test_create_report(self):
        """Тест создания нового отчета."""
        # Вызываем метод create_report
        self.report_db.create_report(code_id=1, feedback="Отличная работа!")

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            INSERT INTO reports (code_id, feedback)
            VALUES (?, ?)
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1, "Отличная работа!"))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_read_report(self):
        """Тест чтения отчета по ID."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchone.return_value = (1, 1, "Отличная работа!")

        # Вызываем метод read_report
        result = self.report_db.read_report(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            SELECT * FROM reports WHERE report_id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, (1, 1, "Отличная работа!"))

    def test_update_report(self):
        """Тест обновления отчета."""
        # Вызываем метод update_report
        self.report_db.update_report(report_id=1, code_id=1, feedback="Можно улучшить.")

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            UPDATE reports
            SET code_id = ?, feedback = ?
            WHERE report_id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1, "Можно улучшить.", 1))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_delete_report(self):
        """Тест удаления отчета."""
        # Вызываем метод delete_report
        self.report_db.delete_report(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            DELETE FROM reports WHERE report_id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_list_reports(self):
        """Тест получения списка всех отчетов."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchall.return_value = [
            (1, 1, "Отличная работа!"),
            (2, 2, "Можно улучшить.")
        ]

        # Вызываем метод list_reports
        result = self.report_db.list_reports()

        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = 'SELECT * FROM reports'
        self.mock_cursor.execute.assert_any_call(expected_query)

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, [
            (1, 1, "Отличная работа!"),
            (2, 2, "Можно улучшить.")
        ])

    def test_close(self):
        """Тест закрытия соединения с базой данных."""
        # Вызываем метод close
        self.report_db.close()

        # Проверяем, что соединение было закрыто
        self.mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()