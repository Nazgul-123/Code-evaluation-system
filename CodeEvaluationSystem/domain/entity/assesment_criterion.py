import sqlite3
from config import DB_PATH

class AssessmentCriterion:
    def __init__(self, db_name=DB_PATH):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Создает таблицу для критериев оценивания, если она не существует."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessment_criteria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (code_id) REFERENCES codes(id)
            )
        ''')
        self.connection.commit()

    def add_criterion(self, code_id: int, content: str):
        """Добавляет новый критерий оценивания в базу данных."""
        self.cursor.execute('''
            INSERT INTO assessment_criteria (code_id, content)
            VALUES (?, ?)
        ''', (code_id, content))
        self.connection.commit()

    def get_criterion(self, criterion_id: int):
        """Получает критерий оценивания по его ID."""
        self.cursor.execute('''
            SELECT * FROM assessment_criteria WHERE id = ?
        ''', (criterion_id,))
        return self.cursor.fetchone()

    def update_criterion(self, criterion_id: int, code_id: int, content: str):
        """Обновляет существующий критерий оценивания."""
        self.cursor.execute('''
            UPDATE assessment_criteria
            SET code_id = ?, content = ?
            WHERE id = ?
        ''', (code_id, content, criterion_id))
        self.connection.commit()

    def delete_criterion(self, criterion_id: int):
        """Удаляет критерий оценивания по его ID."""
        self.cursor.execute('''
            DELETE FROM assessment_criteria WHERE id = ?
        ''', (criterion_id,))
        self.connection.commit()

    def list_criteria(self):
        """Возвращает список всех критериев оценивания."""
        self.cursor.execute('SELECT * FROM assessment_criteria')
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()


# Пример использования
if __name__ == "__main__":
    criterion_db = AssessmentCriterion()

    # Добавление нового критерия оценивания
    criterion_db.add_criterion(code_id=1, content="Код должен компилироваться без ошибок.")

    # Получение критерия по ID
    criterion = criterion_db.get_criterion(1)
    print("Полученный критерий:", criterion)

    # Список всех критериев
    all_criteria = criterion_db.list_criteria()
    print("Все критерии:", all_criteria)

    # Обновление критерия
    criterion_db.update_criterion(criterion_id=1, code_id=1, content="Код должен компилироваться и выполняться корректно.")

    # Получение обновленного критерия
    updated_criterion = criterion_db.get_criterion(1)
    print("Обновленный критерий:", updated_criterion)

    # Удаление критерия
    criterion_db.delete_criterion(1)

    # Закрытие базы данных
    criterion_db.close()
