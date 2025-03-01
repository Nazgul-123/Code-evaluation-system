FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

COPY bot/main.py ./

COPY domain/entity ./domain/entity

# Устанавливаем pip
RUN pip install --upgrade pip

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]