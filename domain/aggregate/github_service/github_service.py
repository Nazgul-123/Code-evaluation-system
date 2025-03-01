import json
import asyncio
import aiormq
from aiormq.abc import DeliveredMessage

RABBITMQ_URL = "amqp://rabbitmq"

async def simulate_github_download(user_id, username):
    """Имитация загрузки кода студента"""
    print(f"Имитация загрузки кода для {username}...")

    # Фейковый код для анализа
    fake_code_files = [
        "using System;\nclass Program { static void Main() { Console.WriteLine(\"Hello, World!\"); } }"
    ]

    await asyncio.sleep(2)  # Имитация задержки

    # Отправляем фейковый код на анализ
    await send_to_analysis(user_id, username, fake_code_files)


async def send_to_analysis(user_id, username, code_files):
    """Отправляет код в очередь на анализ"""
    message = {"user_id": user_id, "username": username, "code_files": code_files}
    connection = await aiormq.connect(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.queue_declare(queue="analysis_queue")
    await channel.basic_publish(
        exchange="",
        routing_key="analysis_queue",
        body=json.dumps(message).encode()
    )
    await connection.close()
    print(f"Фейковый код {username} отправлен в анализ.")


async def process_message(message: DeliveredMessage):
    """Обрабатывает сообщения из очереди `github_queue`"""
    data = json.loads(message.body.decode())
    user_id = data.get("user_id")
    username = data.get("username")

    await simulate_github_download(user_id, username)
    await message.channel.basic_ack(delivery_tag=message.delivery_tag)


async def main():
    """Запуск RabbitMQ consumer"""
    connection = await aiormq.connect(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.queue_declare(queue="github_queue")

    await channel.basic_consume(
        queue="github_queue",
        consumer_callback=process_message,
        no_ack=False,  # Ручное подтверждение сообщений
    )
    print("GitHub-сервис слушает очередь...")
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
