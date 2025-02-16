import telebot
from config import TELEGRAM_TOKEN
from models.static_analyser import evaluate_lab_work_with_static_analyzer
from models.LLM import evaluate_lab_work_with_LLM
from domain.aggregate.report_generation import ReportGenerator

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Словарь для хранения кода пользователей
user_codes = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Я бот для оценки лабораторных работ. "
                          "Отправьте мне ваш код, и я помогу вам с оценкой.")


@bot.message_handler(commands=['evaluate'])
def evaluate_code(message):
    user_id = message.from_user.id

    lab_number = 1
    criteria = "Критерии оценки лабораторной работы:"

    # Проверяем, есть ли у пользователя загруженный код
    if user_id in user_codes:
        code = user_codes[user_id]
        # Оцениваем код с помощью статического анализатора и LLM
        static_analysis_result = evaluate_lab_work_with_static_analyzer(lab_number, code)
        llm_evaluation_result = evaluate_lab_work_with_LLM(lab_number, code, criteria)

        # Генерируем отчет на основе результатов оценки
        report = ReportGenerator.generate_report(
            student_id=user_id,
            LLMAssessment=llm_evaluation_result,
            staticAnalyserAssessment=static_analysis_result
        )

        # Отправляем отчет пользователю
        bot.reply_to(message, report)
    else:
        bot.reply_to(message, "Сначала загрузите ваш код, отправив его в чат.")


@bot.message_handler(func=lambda message: True)
def handle_code_submission(message):
    # Сохраняем код пользователя в словаре
    user_id = message.from_user.id
    user_codes[user_id] = message.text

    # Сообщаем пользователю, что код был загружен
    bot.reply_to(message, "Ваш код успешно загружен! Чтобы получить оценку, введите /evaluate.")


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
