Структура проекта
```
/project-root
│── main.py                     # Точка входа, запуск чат-бот aiogram
│── requirements.txt             # Зависимости Python
│── config.py                     # Конфигурационные файлы
│── domain/                  
│   │── aggregate/                 
│   │   │── cloned_repos    # Директория для работы с форками студентов
│   │   │── github_service.py    # Работа с GitHub
│   │   │── report_generation.py  # Генерация отчетов
│   │── entity/  
│   │   │── repository_settings.py    # Данные общего репозитория для определенной дисциплины
│   │   │── code.py    # Код студента с GitHub
│   │   │── report.py    # Сгенерированный отчет
│   │   │── student.py    # Студент 
│   │   │── teacher.py    # Преподаватель          
│── models/                      # ML-модели для анализа кода, статические анализаторы
│   │── LLM.py       # Языковая модель для оценивавания по заданым критериям
│   │── static_analyser.py       # Статический анализатор для получения метрик по коду
│── tests/                       # Тесты
│   │── e2e/   
│   │── integration/    
│   │── unit/  
│── scripts/                     # Вспомогательные скрипты
│   │── database.py       # Работа с aiosqlite
│── docs/                        # Документация
│── code_evaluation.db       # База данных
```
---

## **Работа с Docker.**
### Запуск контейнера:
1. **Собрать образ**  
   
```sh
   docker build -t aiogram-bot .
```  

2. **Запустить контейнер**  
   
```sh
   docker run --rm -d --name bot aiogram-bot
```  

3. **Логи бота**  
   
```sh
   docker logs -f bot
```  

4. **Остановка контейнера**  
   
```sh
   docker stop bot
```

---

## **Как запустить систему?**
1. **Установите зависимости из requirements.txt**
```commandline
pip install -r requirements.txt
```
2. **Запустите систему**
```commandline
python3 main.py
```
3. **Бот начнет работать**, принимая команды `/start`, `/evaluate`.
   

---

## **Как запускать линтер?**  
1. Установите `Pylint` через команду:  
   
```bash
pip install pylint
```

---

## **Как запускать тесты?**  
1. Установите `pytest` и `pytest-mock`:  
   
```bash
pip install pytest pytest-mock
```

2. Запустите тесты:  
   
```bash
pytest
```

