import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from domain.entity.code import Code  # Импортируем класс Code
from config import DB_PATH  # Импортируем конфигурационные данные


class TestCode(unittest.TestCase):

    @patch('sqlite3.connect')
    def setUp(self, mock_connect):
        """Настройка моков для каждого теста."""
        # Создаем мок для соединения с базой данных
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Создаем экземпляр класса Code
        self.code_db = Code()

    def test_create_code_table(self):
        """Тест создания таблицы codes."""
        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = '''
            CREATE TABLE IF NOT EXISTS codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                lab_number INTEGER NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
            )
        '''
        self.mock_cursor.execute.assert_called_once_with(expected_query)

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called_once()

    def test_create_code(self):
        """Тест создания нового кода."""
        # Вызываем метод create_code
        self.code_db.create_code(student_id=1, lab_number=1, content="print('Hello World')")

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            INSERT INTO codes (student_id, lab_number, content)
            VALUES (?, ?, ?)
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1, 1, "print('Hello World')"))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_read_code(self):
        """Тест чтения кода по ID."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchone.return_value = (1, 1, 1, "print('Hello World')")

        # Вызываем метод read_code
        result = self.code_db.read_code(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            SELECT * FROM codes WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, (1, 1, 1, "print('Hello World')"))

    def test_update_code(self):
        """Тест обновления кода."""
        # Вызываем метод update_code
        self.code_db.update_code(code_id=1, student_id=1, lab_number=2, content="print('Updated Code')")

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            UPDATE codes
            SET student_id = ?, lab_number = ?, content = ?
            WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1, 2, "print('Updated Code')", 1))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_delete_code(self):
        """Тест удаления кода."""
        # Вызываем метод delete_code
        self.code_db.delete_code(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            DELETE FROM codes WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_list_codes(self):
        """Тест получения списка всех кодов."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchall.return_value = [
            (1, 1, 1, "print('Hello World')"),
            (2, 2, 1, "print('Another Code')")
        ]

        # Вызываем метод list_codes
        result = self.code_db.list_codes()

        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = 'SELECT * FROM codes'
        self.mock_cursor.execute.assert_any_call(expected_query)

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, [
            (1, 1, 1, "print('Hello World')"),
            (2, 2, 1, "print('Another Code')")
        ])

    def test_close(self):
        """Тест закрытия соединения с базой данных."""
        # Вызываем метод close
        self.code_db.close()

        # Проверяем, что соединение было закрыто
        self.mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()