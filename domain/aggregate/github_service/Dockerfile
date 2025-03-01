# Используем Python 3.11 в качестве базового образа
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости из корня проекта
COPY requirements.txt ./

RUN pip install --upgrade pip

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код сервиса
COPY domain/aggregate/github_service ./

# Запускаем сервис
CMD ["python", "github_service.py"]