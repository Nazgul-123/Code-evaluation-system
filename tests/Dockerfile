FROM python:3.9

# Устанавливаем зависимости
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY tests ./tests/
COPY domain/entity ./domain/entity


# Запускаем тесты с использованием pytest
CMD ["pytest", "tests", "-v", "--disable-warnings"]