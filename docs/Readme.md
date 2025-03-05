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
Было решено выделить четыре сервиса:
1. Сервис бота
    * Отвечает за запуск чат-бота
2. Сервис анализа кода (code-analysis-service)
    * Отвечает за анализ кода с помощью LLM и статического анализатора.
    * Использует models/LLM.py и models/static_analyser
3. Сервис управления репозиториями (repo-management-service)
   * Работает с форками студентов, загружает их код, хранит данные.
   * Использует domain/aggregate/github_service
4. Сервис для формирования отчетов
   * Использует domain/aggregate/report_service 
github_service клонирует репозитории и отправляет код в analysis_queue.

Сервис анализа кода обрабатывает код и отправляет результаты в report_queue.

report_generation получает результаты и формирует отчеты.

### Запуск микросервиса:
1. **Собрать образ и запустить**  
   
```sh
   docker-compose up -d --build
```  

2. **Остановка контейнеров**  
   
```sh
   docker-compose down
```  

3. **Удалить неактивные образы**  
   
```sh
   docker system prune -f
```  

4. **Просмотреть информацию по контейнерам**  
   
```sh
   docker ps
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

