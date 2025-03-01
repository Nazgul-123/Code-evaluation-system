# Базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости из корня проекта
COPY requirements.txt ./

#RUN pip install --upgrade pip

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код моделей
COPY models /app/models

ENV PYTHONPATH=/app

# Запуск анализатора кода
CMD ["python", "models/analysis_service.py"]
