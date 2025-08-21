Проект состоит из сервера на FastAPI и клиента на PyQt5 для демонстрации взаимодействия через REST API.

## 🏗️ Структура проекта

TestMAST/
├── dist/        # Собранные exe-файлы
│		├── server/
│		│		├── internal/
│		│		└── server.exe
│		└──	client.exe
├── specs/                # Конфиги для сборки
│   ├── server.spec      # Конфиг сборки сервера
│   └── client.spec      # Конфиг сборки клиента
├── src/                    
│   ├── server/            # Серверная часть
│   │		├──		routers/		 # Маршрутизация 
│   │		│		└── items.py
│   │   ├── __init__.py
│   │   ├── main.py        # Основной файл сервера
│   │   ├── database.py    # Настройки базы данных
│   │   └── models.py      # Модели данных 
│   └── client/            # Клиентская часть (PyQt5)
│       ├── __init__.py
│       ├── main.py        # Точка входа клиента
│       ├── app.py         # Основной класс приложения
│       └── api_client.py  # Клиент для работы с API
├── tests/                 # Тесты
│   ├── test_server.py    # Тесты сервера
│   └── test_client.py    # Тесты клиента
├──	.gitignore
├── pytest.ini
└── README.md            # Эта документация

## 📦 Зависимости

### Сервер
- `fastapi==0.104.1` - Веб-фреймворк
- `uvicorn==0.24.0` - ASGI-сервер
- `sqlalchemy==2.0.23` - ORM для БД
- `pydantic==2.5.0` - Валидация данных

### Клиент
- `PyQt5==5.15.9` - GUI фреймворк
- `requests==2.31.0` - HTTP-клиент

### Тестирование
- `pytest==7.4.3` - Фреймворк тестирования
- `pytest-qt==4.2.0` - Тестирование PyQt

### Сборка в exe-файлы
- `pyinstaller`


# Запуск сервера
### Способ 1: Через Python
`python -m src.server.main`

### Способ 2: Через uvicorn
`uvicorn src.server.main:app --reload`

# Запуск клиента
`python -m src.client.main`