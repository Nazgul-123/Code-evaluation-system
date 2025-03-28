Структура проекта
```
/project-root
│── .github/                  
│   │── workflows/                 
│   │   │── ci.yaml    # Директория для работы с форками студентов
│── bot/    
│   │── main.py                     # Точка входа, запуск чат-бот aiogram
│   │── Dockerfile                     
│   │── code_evaluation.db                     # База данных
│── requirements.txt             # Зависимости Python
│── config.py                     # Конфигурационные файлы
│── domain/                  
│   │── aggregate/        
│   │   │── github_service/    # Работа с GitHub         
│   │   │   │── cloned_repos    # Директория для работы с форками студентов
│   │   │   │── Dockerfile    
│   │   │   │── github_service.py    # Скачивание работ с гх и их обработка
│   │   │── report_service/    # Генерация отчета         
│   │   │   │── report_generation.py  
│   │   │   │── Dockerfile    
│   │── entity/  
│   │   │── assessment_criterion.py    # Критерии проверки 
│   │   │── code.py    # Код студента с GitHub
│   │   │── report.py    # Сгенерированный отчет
│   │   │── repository_settings.py    # Данные общего репозитория для определенной дисциплины
│   │   │── student.py    # Студент 
│   │   │── teacher.py    # Преподаватель          
│── models/                      # ML-модели для анализа кода, статические анализаторы
│   │── analysis_service.py       # Обработка результатов оценки
│   │── LLM.py       # Языковая модель для оценивавания по заданым критериям
│   │── static_analyser.py       # Статический анализатор для получения метрик по коду
│   │── Dockerfile                     
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

