#тесты для классов assesment_criterion, code, report, student, teacher
import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from domain.entity.assesment_criterion import AssessmentCriterion  # Импортируем класс AssessmentCriterion
from config import DB_PATH  # Импортируем конфигурационные данные

class TestAssessmentCriterion(unittest.TestCase):

    @patch('sqlite3.connect')
    def setUp(self, mock_connect):
        """Настройка моков для каждого теста."""
        # Создаем мок для соединения с базой данных
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Создаем экземпляр класса AssessmentCriterion
        self.criterion_db = AssessmentCriterion()

    def test_create_table(self):
        """Тест создания таблицы assessment_criteria."""
        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = '''
            CREATE TABLE IF NOT EXISTS assessment_criteria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (code_id) REFERENCES codes(id)
            )
        '''
        self.mock_cursor.execute.assert_called_once_with(expected_query)

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called_once()

    def test_add_criterion(self):
        """Тест добавления нового критерия оценивания."""
        # Вызываем метод add_criterion
        self.criterion_db.add_criterion(code_id=1, content="Код должен компилироваться без ошибок.")

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            INSERT INTO assessment_criteria (code_id, content)
            VALUES (?, ?)
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1, "Код должен компилироваться без ошибок."))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_get_criterion(self):
        """Тест получения критерия по ID."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchone.return_value = (1, 1, "Код должен компилироваться без ошибок.")

        # Вызываем метод get_criterion
        result = self.criterion_db.get_criterion(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            SELECT * FROM assessment_criteria WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, (1, 1, "Код должен компилироваться без ошибок."))

    def test_update_criterion(self):
        """Тест обновления критерия оценивания."""
        # Вызываем метод update_criterion
        self.criterion_db.update_criterion(criterion_id=1, code_id=1, content="Код должен компилироваться и выполняться корректно.")

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            UPDATE assessment_criteria
            SET code_id = ?, content = ?
            WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1, "Код должен компилироваться и выполняться корректно.", 1))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_delete_criterion(self):
        """Тест удаления критерия оценивания."""
        # Вызываем метод delete_criterion
        self.criterion_db.delete_criterion(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            DELETE FROM assessment_criteria WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_list_criteria(self):
        """Тест получения списка всех критериев оценивания."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchall.return_value = [
            (1, 1, "Код должен компилироваться без ошибок."),
            (2, 1, "Код должен быть читаемым.")
        ]

        # Вызываем метод list_criteria
        result = self.criterion_db.list_criteria()

        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = 'SELECT * FROM assessment_criteria'
        self.mock_cursor.execute.assert_any_call(expected_query)

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, [
            (1, 1, "Код должен компилироваться без ошибок."),
            (2, 1, "Код должен быть читаемым.")
        ])

    def test_close(self):
        """Тест закрытия соединения с базой данных."""
        # Вызываем метод close
        self.criterion_db.close()

        # Проверяем, что соединение было закрыто
        self.mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()