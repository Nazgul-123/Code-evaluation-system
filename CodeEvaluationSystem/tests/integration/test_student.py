import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from domain.entity.student import Student  # Импортируем класс Student
from config import DB_PATH  # Импортируем конфигурационные данные


class TestStudent(unittest.TestCase):

    @patch('sqlite3.connect')
    def setUp(self, mock_connect):
        """Настройка моков для каждого теста."""
        # Создаем мок для соединения с базой данных
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Создаем экземпляр класса Student
        self.student_db = Student()

    def test_create_table(self):
        """Тест создания таблицы students."""
        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = '''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                group_number TEXT NOT NULL,
                github_username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        '''
        self.mock_cursor.execute.assert_called_once_with(expected_query)

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called_once()

    def test_create_student(self):
        """Тест создания нового студента."""
        # Вызываем метод create_student
        self.student_db.create_student(
            full_name="Иван Иванов",
            group_number="Группа 101",
            github_username="ivanov",
            email="ivanov@example.com"
        )

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            INSERT INTO students (full_name, group_number, github_username, email)
            VALUES (?, ?, ?, ?)
        '''
        self.mock_cursor.execute.assert_any_call(
            expected_query,
            ("Иван Иванов", "Группа 101", "ivanov", "ivanov@example.com")
        )

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_read_student(self):
        """Тест чтения студента по ID."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchone.return_value = (
            1, "Иван Иванов", "Группа 101", "ivanov", "ivanov@example.com"
        )

        # Вызываем метод read_student
        result = self.student_db.read_student(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            SELECT * FROM students WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(
            result,
            (1, "Иван Иванов", "Группа 101", "ivanov", "ivanov@example.com")
        )

    def test_update_student(self):
        """Тест обновления данных студента."""
        # Вызываем метод update_student
        self.student_db.update_student(
            student_id=1,
            full_name="Петр Петров",
            group_number="Группа 102",
            github_username="petrov",
            email="petrov@example.com"
        )

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            UPDATE students
            SET full_name = ?, group_number = ?, github_username = ?, email = ?
            WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(
            expected_query,
            ("Петр Петров", "Группа 102", "petrov", "petrov@example.com", 1)
        )

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_delete_student(self):
        """Тест удаления студента по ID."""
        # Вызываем метод delete_student
        self.student_db.delete_student(1)

        # Проверяем, что метод execute был вызван с правильными параметрами
        expected_query = '''
            DELETE FROM students WHERE id = ?
        '''
        self.mock_cursor.execute.assert_any_call(expected_query, (1,))

        # Проверяем, что изменения были зафиксированы
        self.mock_connection.commit.assert_called()

    def test_list_students(self):
        """Тест получения списка всех студентов."""
        # Настраиваем мок для возврата данных
        self.mock_cursor.fetchall.return_value = [
            (1, "Иван Иванов", "Группа 101", "ivanov", "ivanov@example.com"),
            (2, "Петр Петров", "Группа 102", "petrov", "petrov@example.com")
        ]

        # Вызываем метод list_students
        result = self.student_db.list_students()

        # Проверяем, что метод execute был вызван с правильным SQL-запросом
        expected_query = 'SELECT * FROM students'
        self.mock_cursor.execute.assert_any_call(expected_query)

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(
            result,
            [
                (1, "Иван Иванов", "Группа 101", "ivanov", "ivanov@example.com"),
                (2, "Петр Петров", "Группа 102", "petrov", "petrov@example.com")
            ]
        )

    def test_close(self):
        """Тест закрытия соединения с базой данных."""
        # Вызываем метод close
        self.student_db.close()

        # Проверяем, что соединение было закрыто
        self.mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()