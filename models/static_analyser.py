import asyncio


async def analyze_code_with_static_analyzer(code: str) -> dict:
    """
    Асинхронно выполняет статический анализ кода и возвращает метрики.

    :param code: Текст кода
    :return: Словарь с метриками кода
    """
    # Имитация задержки работы анализатора (например, вызов внешнего API)
    await asyncio.sleep(1)

    # Заглушка для статического анализа
    metrics = {
        "lines_of_code": 100,
        "cyclomatic_complexity": 10,
        "num_functions": 5,
        "num_classes": 2,
        "code_smells": ["Неправильное имя переменной", "Дублирование кода"],
    }
    return metrics


async def evaluate_lab_work_with_static_analyzer(lab_number: int, code: str) -> str:
    """
    Асинхронно оценивает код лабораторной работы и возвращает метрики.

    :param lab_number: Номер лабораторной работы
    :param code: Текст кода лабораторной работы
    :return: Строка с метриками кода
    """
    # Получаем метрики с помощью статического анализатора
    metrics = await analyze_code_with_static_analyzer(code)

    # Формируем отчет о метриках
    evaluated_report = f"Результат работы статического анализатора по лабораторной работе №{lab_number}:\n\n"
    evaluated_report += f"Количество строк кода: {metrics['lines_of_code']}\n"
    evaluated_report += f"Цикломатическая сложность: {metrics['cyclomatic_complexity']}\n"
    evaluated_report += f"Количество функций: {metrics['num_functions']}\n"
    evaluated_report += f"Количество классов: {metrics['num_classes']}\n"
    evaluated_report += f"Проблемы кода: {', '.join(metrics['code_smells'])}\n"

    return evaluated_report


# Пример асинхронного использования
async def main():
    lab_number = 1
    code = "Пример кода"
    result = await evaluate_lab_work_with_static_analyzer(lab_number, code)
    print(f"Результат: {result}")


if __name__ == "__main__":
    asyncio.run(main())