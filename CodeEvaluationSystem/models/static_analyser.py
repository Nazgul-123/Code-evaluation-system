#здесь будет импортироваться и использоваться статический анализатор для получения метрик

def analyze_code_with_static_analyzer(code: str) -> dict:
    """
    Выполняет статический анализ кода и возвращает метрики.

    :param code: Текстовый файл с кодом
    :return: Словарь с метриками кода
    """
    # Здесь должен быть вызов статического анализатора
    # Для примера, просто создадим заглушку метрик
    metrics = {
        "lines_of_code": 100,  # Пример: количество строк кода
        "cyclomatic_complexity": 10,  # Пример: цикломатическая сложность
        "num_functions": 5,  # Пример: количество функций
        "num_classes": 2,  # Пример: количество классов
        "code_smells": ["Неправильное имя переменной", "Дублирование кода"],  # Пример: выявленные проблемы
    }

    return metrics


def evaluate_lab_work_with_static_analyzer(lab_number: int, code: str) -> str:
    """
    Оценивает код лабораторной работы и возвращает метрики.

    :param lab_number: Номер лабораторной работы
    :param code: Текстовый файл с кодом
    :return: Текстовый файл с метриками
    """

    # Получение метрик с помощью статического анализатора
    metrics = analyze_code_with_static_analyzer(code)

    # Формирование отчета о метриках
    evaluated_report = f"Результат работы статического анализатора по лабораторной работе №{lab_number}:\n\n"
    evaluated_report += f"Количество строк кода: {metrics['lines_of_code']}\n"
    evaluated_report += f"Цикломатическая сложность: {metrics['cyclomatic_complexity']}\n"
    evaluated_report += f"Количество функций: {metrics['num_functions']}\n"
    evaluated_report += f"Количество классов: {metrics['num_classes']}\n"
    evaluated_report += f"Проблемы кода: {', '.join(metrics['code_smells'])}\n"

    return evaluated_report


# Пример использования функции
if __name__ == "__main__":
    lab_number = 1
    code = "Пример кода"
    result = evaluate_lab_work_with_static_analyzer(lab_number, code)
    print(f"Результат: {result}")
