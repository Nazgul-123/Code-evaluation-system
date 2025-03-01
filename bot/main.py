import asyncio
import json
import aiormq
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv
from aiormq.abc import DeliveredMessage
from typing import Coroutine
import json

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
RABBITMQ_URL = "amqp://rabbitmq"

if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения!")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Кнопка для получения отчета
def get_report_button():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Получить отчет по коду студента")]  # Передаём кнопки сразу в конструктор
        ],
        resize_keyboard=True
    )
    return keyboard

# Отправка сообщений в RabbitMQ
async def send_to_queue(queue_name, message):
    connection = await aiormq.connect(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.queue_declare(queue=queue_name)
    await channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message).encode()
    )
    await connection.close()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    """Приветственное сообщение с кнопкой"""
    await message.answer(
        "Добро пожаловать! Нажмите кнопку ниже, чтобы получить отчет по коду студента.",
        reply_markup=get_report_button()
    )

@dp.message(lambda message: message.text == "Получить отчет по коду студента")
async def handle_report_request(message: Message):
    """Обрабатывает нажатие кнопки 'Получить отчет'"""
    user_id = message.from_user.id
    username = message.from_user.username #здесь будет извлечение имени пользователя в гитхабе


    # Отправляем запрос в очередь GitHub сервиса для получения кода
    await send_to_queue("github_queue", {"user_id": user_id, "username": username})

    await message.answer("Ваш код отправлен на проверку. Ожидайте результат...")

async def process_report(message: DeliveredMessage):
    """Получает отчет из `bot_queue` и отправляет студенту"""
    # Декодируем тело сообщения (оно приходит в виде bytes)
    data = json.loads(message.body.decode())

    # Извлекаем данные
    user_id = data["user_id"]
    report = data["report"]

    # Отправляем сообщение студенту
    await bot.send_message(
        chat_id=user_id,
        text=report,
        parse_mode="Markdown",
        reply_markup=get_report_button()
    )

    # Подтверждаем обработку сообщения
    await message.channel.basic_ack(delivery_tag=message.delivery_tag)

async def consume_bot_queue():
    """Ожидает отчет из `bot_queue` и отправляет его студенту"""
    connection = await aiormq.connect(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.queue_declare(queue="bot_queue")

    await channel.basic_consume(queue="bot_queue", consumer_callback=process_report)
    print("Бот слушает очередь `bot_queue`...")

async def main():
    print("Бот запущен...")
    await asyncio.gather(
        dp.start_polling(bot),
        consume_bot_queue()
    )

if __name__ == "__main__":
    asyncio.run(main())
