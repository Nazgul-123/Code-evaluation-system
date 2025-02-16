Структура проекта
```
/project-root
│── main.py                     # Точка входа
│── requirements.txt             # Зависимости Python
│── config/                      # Конфигурационные файлы
│── domain/                  
│   │── aggregate/                 
│   │   │── github_service.py    # Работа с GitHub
│   │   │── report_generation.py  # Генерация отчетов
│   │── entity/  
│   │   │── admin.py    
│   │   │── code.py    # Код студента с GitHub
│   │   │── report.py    # Сгенерированный отчет
│   │   │── student.py    
│   │   │── teacher.py                
│── models/                      # ML-модели для анализа кода, статические анализаторы
│── tests/                       # Тесты
│── scripts/                     # Вспомогательные скрипты
│   │── database.py       # Работа с SQLite
│── docs/                        # Документация
```

---

## **Как запустить систему?**
1. **Установите зависимости из requirements.txt**
```commandline
pip install -r requirements.txt
```
2. **Запустите систему**
```commandline
python main.py
```
3. **Бот начнет работать**, принимая команды `/start`, `/upload` и `/report`.
   

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
pytest tests/
```

