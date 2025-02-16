import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from domain.entity.teacher import Teacher  # Импортируем класс Teacher
from config import DB_PATH  # Импортируем конфигурационные данные


class TestTeacher(unittest.TestCase):

    @patch('sqlite3.connect')
    def setUp(self, mock_connect):
        """Настройка моков для каждого теста."""
        # Создаем мок для соединения с базой данных
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Создаем экземпляр класса Teacher
        self.teacher_db = Teacher()

    def test_create_table(self):
        """Тест создания таблицы teachers."""
        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = '''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        '''
        self.mock_cursor.execute.assert_called_once_with(expected_query)

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called_once()

    def test_create_teacher(self):
        """Тест создания нового преподавателя."""
        # Вызываем метод create_teacher
        self.teacher_db.create_teacher(
            full_name="Иван Иванов",
            email="ivanov@example.com"
        )

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            INSERT INTO teachers (full_name, email)
            VALUES (?, ?)
        '''
        self.mock_cursor.execute.assert_any_call(
            expected_query,
            ("Иван Иванов", "ivanov@example.com")
        )

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_read_teacher(self):
        """Тест чтения преподавателя по ID."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchone.return_value = (
            1, "Иван Иванов", "ivanov@example.com"
        )

        # Вызываем метод read_teacher
        result = self.teacher_db.read_teacher(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            SELECT * FROM teachers WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(
            result,
            (1, "Иван Иванов", "ivanov@example.com")
        )

    def test_update_teacher(self):
        """Тест обновления данных преподавателя."""
        # Вызываем метод update_teacher
        self.teacher_db.update_teacher(
            teacher_id=1,
            full_name="Петр Петров",
            email="petrov@example.com"
        )

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            UPDATE teachers
            SET full_name = ?, email = ?
            WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(
            expected_query,
            ("Петр Петров", "petrov@example.com", 1)
        )

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_delete_teacher(self):
        """Тест удаления преподавателя по ID."""
        # Вызываем метод delete_teacher
        self.teacher_db.delete_teacher(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            DELETE FROM teachers WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_list_teachers(self):
        """Тест получения списка всех преподавателей."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchall.return_value = [
            (1, "Иван Иванов", "ivanov@example.com"),
            (2, "Петр Петров", "petrov@example.com")
        ]

        # Вызываем метод list_teachers
        result = self.teacher_db.list_teachers()

        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = 'SELECT * FROM teachers'
        self.mock_cursor.execute.assert_any_call(expected_query)

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(
            result,
            [
                (1, "Иван Иванов", "ivanov@example.com"),
                (2, "Петр Петров", "petrov@example.com")
            ]
        )

    def test_close(self):
        """Тест закрытия соединения с базой данных."""
        # Вызываем метод close
        self.teacher_db.close()

        # Проверяем, что соединение было закрыто
        self.mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()