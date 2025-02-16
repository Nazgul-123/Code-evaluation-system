import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from config import TELEGRAM_TOKEN
from models.static_analyser import evaluate_lab_work_with_static_analyzer
from models.LLM import evaluate_lab_work_with_LLM
from domain.aggregate.report_generation import ReportGenerator

# Создаем объект бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Словарь для хранения кода пользователей
user_codes = {}

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Добро пожаловать! Я бот для оценки лабораторных работ. "
                         "Отправьте мне ваш код, и я помогу вам с оценкой.")

@dp.message(Command("evaluate"))
async def evaluate_code(message: Message):
    user_id = message.from_user.id
    lab_number = 1
    criteria = "Критерии оценки лабораторной работы:"

    # Проверяем, есть ли у пользователя загруженный код
    if user_id in user_codes:
        code = user_codes[user_id]

        # Оцениваем код с помощью статического анализатора и LLM
        static_analysis_result = await evaluate_lab_work_with_static_analyzer(lab_number, code)
        llm_evaluation_result = await evaluate_lab_work_with_LLM(lab_number, code, criteria)

        # Генерируем отчет на основе результатов оценки
        report = await ReportGenerator.generate_report(
            student_id=str(user_id),
            LLMAssessment=llm_evaluation_result,
            staticAnalyserAssessment=static_analysis_result
        )

        # Отправляем отчет пользователю
        await message.answer(report)
    else:
        await message.answer("Сначала загрузите ваш код, отправив его в чат.")

@dp.message()
async def handle_code_submission(message: Message):
    # Сохраняем код пользователя в словаре
    user_id = message.from_user.id
    user_codes[user_id] = message.text

    # Сообщаем пользователю, что код был загружен
    await message.answer("Ваш код успешно загружен! Чтобы получить оценку, введите /evaluate.")

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())