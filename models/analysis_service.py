import json
import asyncio
import aiormq
from models.static_analyser import evaluate_lab_work_with_static_analyzer
from models.LLM import evaluate_lab_work_with_LLM
from aiormq.abc import DeliveredMessage

RABBITMQ_URL = "amqp://rabbitmq"

async def analyze_static_code(code):
    """Анализирует код статическим анализатором"""
    try:
        result = await evaluate_lab_work_with_static_analyzer(lab_number=1,  code=code)
        return json.dumps(result, ensure_ascii=False, indent=2).replace("\\n", "\n")  # Преобразуем в строку
    except Exception as e:
        return f"Ошибка статического анализа: {e}"

async def analyze_with_llm(code):
    """Анализирует код LLM"""
    try:
        result = await evaluate_lab_work_with_LLM(lab_number=1, code=code, criteria="Критерии оценки")
        return json.dumps(result, ensure_ascii=False, indent=2).replace("\\n", "\n")  # Преобразуем в строку
    except Exception as e:
        return f"Ошибка анализа LLM: {e}"

async def process_message(message: DeliveredMessage):
    """Обрабатывает сообщения из `analysis_queue`"""
    data = json.loads(message.body.decode())
    user_id = data["user_id"]
    username = data["username"]
    code_files = data["code_files"]

    # Запускаем анализ всех файлов параллельно и ждем завершения
    static_analysis_results = await asyncio.gather(*(analyze_static_code(code) for code in code_files))
    llm_analysis_results = await asyncio.gather(*(analyze_with_llm(code) for code in code_files))

    # Объединяем результаты в один отчет
    static_analysis = "\n\n".join(static_analysis_results) if static_analysis_results else None
    llm_assessment = "\n\n".join(llm_analysis_results) if llm_analysis_results else None

    # Отправляем один отчет в `report_queue`
    await send_to_report_queue(user_id, username, static_analysis, llm_assessment)

    await message.channel.basic_ack(delivery_tag=message.delivery_tag)

async def send_to_report_queue(user_id, username, static_analysis=None, llm_assessment=None):
    """Отправляет результаты анализа в `report_queue`"""
    message = {"user_id": user_id, "username": username}

    if static_analysis:
        message["staticAnalyserAssessment"] = static_analysis
    if llm_assessment:
        message["LLMAssessment"] = llm_assessment

    connection = await aiormq.connect(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.queue_declare(queue="report_queue")
    await channel.basic_publish(
        exchange="",
        routing_key="report_queue",
        body=json.dumps(message).encode()
    )
    await connection.close()
    print(f"Анализ {username}: отчет отправлен в report_queue")

async def main():
    """Запуск RabbitMQ consumer"""
    connection = await aiormq.connect(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.queue_declare(queue="analysis_queue")

    await channel.basic_consume(
        queue="analysis_queue",
        consumer_callback=process_message,
        no_ack=False,  # Ручное подтверждение сообщений
    )
    print("Сервис анализа кода слушает очередь `analysis_queue`...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
