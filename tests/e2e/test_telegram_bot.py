import asyncio
import json
import pytest
from datetime import datetime
from aiogram import Bot
from aiogram.types import Message, Chat, User
from aiormq import connect
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
RABBITMQ_URL = "amqp://rabbitmq"

@pytest.mark.asyncio
async def test_end_to_end():
    """Проверяет полный процесс от отправки команды боту до получения отчета"""

    # Отправляем команду в бота
    bot = Bot(token=TELEGRAM_TOKEN)
    user_id = 123456  # Имитируем ID пользователя
    username = "test_user"

    message = Message(
        message_id=1,
        date=datetime.now(),
        chat=Chat(id=user_id, type="private"),
        from_user=User(id=user_id, is_bot=False, username=username, first_name="Test"),
        text="Получить отчет по коду студента"
    )

    try:
        # Подключаемся к RabbitMQ
        connection = await connect(RABBITMQ_URL)
        channel = await connection.channel()

        # Бот должен отправить запрос в `github_queue`
        await channel.queue_declare(queue="github_queue")
        await channel.basic_publish(
            exchange="",
            routing_key="github_queue",
            body=json.dumps({"user_id": user_id, "username": username}).encode()
        )
        print("Запрос отправлен в github_queue")

        # Ждём, пока `GitHub Service` получит код и отправит его в `analysis_queue`
        await asyncio.sleep(2)  # Имитация обработки

        # Создаем очередь для анализа
        await channel.queue_declare(queue="analysis_queue")

        # Используем Future для ожидания сообщения
        analysis_future = asyncio.Future()

        # Callback-функция для обработки сообщений из analysis_queue
        async def analysis_callback(message):
            print("Получено сообщение в analysis_queue")
            data = json.loads(message.body.decode())
            assert data["user_id"] == user_id
            print("GitHub Service обработал код и передал его в analysis_queue")
            analysis_future.set_result(data)

        # Подписываемся на очередь analysis_queue
        await channel.basic_consume(queue="analysis_queue", consumer_callback=analysis_callback, no_ack=True)

        # Ждем завершения Future с таймаутом
        try:
            await asyncio.wait_for(analysis_future, timeout=10.0)
        except asyncio.TimeoutError:
            pytest.fail("Сообщение в analysis_queue не было получено вовремя")

        # Ждём, пока `Analysis Service` проанализирует код и отправит результат в `report_queue`
        await asyncio.sleep(2)

        # Создаем очередь для отчетов
        await channel.queue_declare(queue="report_queue")

        # Используем Future для ожидания сообщения
        report_future = asyncio.Future()

        # Callback-функция для обработки сообщений из report_queue
        async def report_callback(message):
            print("Получено сообщение в report_queue")
            data = json.loads(message.body.decode())
            assert data["user_id"] == user_id
            assert "staticAnalyserAssessment" in data
            assert "LLMAssessment" in data
            print("Analysis Service отправил результаты анализа в report_queue")
            report_future.set_result(data)

        # Подписываемся на очередь report_queue
        await channel.basic_consume(queue="report_queue", consumer_callback=report_callback, no_ack=True)

        # Ждем завершения Future с таймаутом
        try:
            await asyncio.wait_for(report_future, timeout=10.0)
        except asyncio.TimeoutError:
            pytest.fail("Сообщение в report_queue не было получено вовремя")

        # Ждём, пока `Report Service` отправит отчет в `bot_queue`
        await asyncio.sleep(2)

        # Создаем очередь для бота
        await channel.queue_declare(queue="bot_queue")

        # Используем Future для ожидания сообщения
        bot_future = asyncio.Future()

        # Callback-функция для обработки сообщений из bot_queue
        async def bot_callback(message):
            print("Получено сообщение в bot_queue")
            data = json.loads(message.body.decode())
            assert data["user_id"] == user_id
            assert "report" in data
            print("Report Service отправил отчет в bot_queue")
            bot_future.set_result(data)

        # Подписываемся на очередь bot_queue
        await channel.basic_consume(queue="bot_queue", consumer_callback=bot_callback, no_ack=True)

        # Ждем завершения Future с таймаутом
        try:
            await asyncio.wait_for(bot_future, timeout=10.0)
        except asyncio.TimeoutError:
            pytest.fail("Сообщение в bot_queue не было получено вовремя")

        # Бот должен получить отчет и отправить его пользователю
        received_report = bot_future.result()["report"]
        assert "Оценка ИИ" in received_report
        assert "Результаты статического анализатора" in received_report
        print("Бот успешно получил и отправил отчет пользователю")
    except Exception as e:
        print(f"Ошибка {e}")