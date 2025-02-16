class ReportGenerator:
    @staticmethod
    def generate_report(student_id: str, LLMAssessment: str, staticAnalyserAssessment: str) -> str:
        """ Генерирует отчет по коду результатам работы LLM и статического анализатора и возвращает его в текстовом виде """
        # Генерируем отчет
        return f"Отчет по коду студента{student_id}: \n {LLMAssessment} \n {staticAnalyserAssessment}"

    @staticmethod
    def generate_reports(codes: list) -> list:
        """ Принимает список кодов и генерирует отчеты по каждому из них """
        reports = []
        for code in codes:
            report = ReportGenerator.generate_report(code)
            reports.append(report)
        return reports