import json
import asyncio
import aiormq
from aiormq.abc import DeliveredMessage

RABBITMQ_URL = "amqp://rabbitmq"

# Хранилище для временного хранения частичных результатов анализа
analysis_results = {}


class ReportGenerator:
    @staticmethod
    async def generate_report(student_id: str, LLMAssessment: str, staticAnalyserAssessment: str) -> str:
        """Генерирует отчет по коду с результатами LLM и статического анализатора."""
        return (f"📊 *Отчет по коду студента {student_id}:*\n\n"
                f"🤖 *Оценка ИИ:* {LLMAssessment}\n"
                f"🛠 *Результаты статического анализатора:* {staticAnalyserAssessment}\n")


async def send_to_bot_queue(user_id, report):
    """Отправляет отчет в `bot_queue`, чтобы бот мог отправить его студенту."""
    connection = await aiormq.connect(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.queue_declare(queue="bot_queue")
    message = {"user_id": user_id, "report": report}
    await channel.basic_publish(
        exchange="",
        routing_key="bot_queue",
        body=json.dumps(message).encode()
    )
    await connection.close()


async def process_message(message: DeliveredMessage):
    """Обрабатывает входящее сообщение с результатами анализа."""
    data = json.loads(message.body.decode())
    user_id = data["user_id"]
    username = data["username"]

    # Обновляем данные в хранилище
    if user_id not in analysis_results:
        analysis_results[user_id] = {"username": username, "LLMAssessment": None, "staticAnalyserAssessment": None}

    if "LLMAssessment" in data:
        analysis_results[user_id]["LLMAssessment"] = data["LLMAssessment"]
    if "staticAnalyserAssessment" in data:
        analysis_results[user_id]["staticAnalyserAssessment"] = data["staticAnalyserAssessment"]

    # Проверяем, готовы ли оба анализа
    if (analysis_results[user_id]["LLMAssessment"] is not None and
            analysis_results[user_id]["staticAnalyserAssessment"] is not None):
        # Формируем отчет
        report = await ReportGenerator.generate_report(
            username,
            analysis_results[user_id]["LLMAssessment"],
            analysis_results[user_id]["staticAnalyserAssessment"]
        )

        # Отправляем отчет в `bot_queue`
        await send_to_bot_queue(user_id, report)

        # Удаляем обработанный результат
        del analysis_results[user_id]

    await message.channel.basic_ack(delivery_tag=message.delivery_tag)


async def main():
    """Запуск RabbitMQ consumer"""
    connection = await aiormq.connect(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.queue_declare(queue="report_queue")

    await channel.basic_consume(
        queue="report_queue",
        consumer_callback=process_message,
        no_ack=False,  # Ручное подтверждение сообщений
    )
    print("Report-сервис слушает очередь `report_queue`...")
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
