import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.server.main import app
from src.server.database import Base, get_db

# Настройка тестовой БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_client():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Переопределяем зависимость БД
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    # Очистка после тестов
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

def test_create_item(test_client):
    """Тест создания элемента"""
    response = test_client.post(
        "/items/",
        json={"description": "Первый", "day": "15.08.2025", "time": "15:43", "click_number": 1}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Первый"

def test_get_items(test_client):
    """Тест получения элементов"""
    # Сначала создаем элемент
    test_client.post("/items/", json={"description": "Первый", "day": "15.08.2025", "time": "15:43", "click_number": 1})
    
    response = test_client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_pagination(test_client):
    """Тест пагинации"""
    # Создаем 3 элемента
    for i in range(3):
        test_client.post("/items/", json={"description": "Первый", "day": "15.08.2025", "time": "15:43", "click_number": i})
    
    response = test_client.get("/items/?skip=1&limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1 & response.json()[0]["click_number"] == 1