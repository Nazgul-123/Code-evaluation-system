import sqlite3
from config import DB_PATH

class Report:
    def __init__(self, db_name=DB_PATH):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_report_table()

    def create_report_table(self):
        """Создает таблицу отчетов, если она не существует."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_id INTEGER NOT NULL,
                feedback TEXT NOT NULL,
                FOREIGN KEY (code_id) REFERENCES codes (id) ON DELETE CASCADE
            )
        ''')
        self.connection.commit()

    def create_report(self, code_id: int, feedback: str):
        """Создает новый отчет в базе данных."""
        self.cursor.execute('''
            INSERT INTO reports (code_id, feedback)
            VALUES (?, ?)
        ''', (code_id, feedback))
        self.connection.commit()

    def read_report(self, report_id: int):
        """Читает данные отчета по его ID."""
        self.cursor.execute('''
            SELECT * FROM reports WHERE report_id = ?
        ''', (report_id,))
        return self.cursor.fetchone()

    def update_report(self, report_id: int, code_id: int, feedback: str):
        """Обновляет данные отчета."""
        self.cursor.execute('''
            UPDATE reports
            SET code_id = ?, feedback = ?
            WHERE report_id = ?
        ''', (code_id, feedback, report_id))
        self.connection.commit()

    def delete_report(self, report_id: int):
        """Удаляет отчет по его ID."""
        self.cursor.execute('''
            DELETE FROM reports WHERE report_id = ?
        ''', (report_id,))
        self.connection.commit()

    def list_reports(self):
        """Возвращает список всех отчетов."""
        self.cursor.execute('SELECT * FROM reports')
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()


# Пример использования
if __name__ == "__main__":
    report_db = Report()

    # Создание отчета
    report_db.create_report(1, "Отличная работа!")

    # Чтение отчета
    report = report_db.read_report(1)
    print("Отчет:", report)

    # Список отчетов
    all_reports = report_db.list_reports()
    print("Все отчеты:", all_reports)

    # Закрытие базы данных
    report_db.close()
