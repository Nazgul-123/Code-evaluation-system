class ReportGenerator:
    @staticmethod
    async def generate_report(student_id: str, LLMAssessment: str, staticAnalyserAssessment: str) -> str:
        """ Генерирует отчет по коду результатам работы LLM и статического анализатора и возвращает его в текстовом виде """
        # Генерируем отчет
        return f"Отчет по коду студента {student_id}: \n{LLMAssessment} \n{staticAnalyserAssessment}"

    @staticmethod
    async def generate_reports(codes: list) -> list:
        """ Принимает список кодов и генерирует отчеты по каждому из них """
        reports = []
        for code in codes:
            # Используем await для вызова асинхронного метода
            report = await ReportGenerator.generate_report(
                code['student_id'],
                code['LLMAssessment'],
                code['staticAnalyserAssessment']
            )
            reports.append(report)
        return reports


# Пример использования
async def main():
    codes = [
        {'student_id': '1', 'LLMAssessment': 'Результат LLM 1',
         'staticAnalyserAssessment': 'Результат статического анализатора 1'},
        {'student_id': '2', 'LLMAssessment': 'Результат LLM 2',
         'staticAnalyserAssessment': 'Результат статического анализатора 2'},
    ]

    reports = await ReportGenerator.generate_reports(codes)
    for report in reports:
        print(report)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
