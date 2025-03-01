FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости из корня проекта
COPY requirements.txt ./

RUN pip install --upgrade pip

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код сервиса
COPY domain/aggregate/report_service ./

CMD ["python", "report_generation.py"]