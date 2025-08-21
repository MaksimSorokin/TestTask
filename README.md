Проект состоит из сервера на FastAPI и клиента на PyQt5 для демонстрации взаимодействия через REST API.

## 🏗️ Структура проекта

<img width="859" height="698" alt="image" src="https://github.com/user-attachments/assets/fcb7026f-9553-4119-ba69-b5bac733f084" />


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
