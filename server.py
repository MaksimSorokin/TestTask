from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from sqlalchemy.orm import Session

# Инициализация FastAPI
app = FastAPI()

# Настройка SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модель для базы данных
class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    day = Column(String)
    time = Column(String)
    click_number = Column(Integer)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Pydantic модели для валидации
class ItemCreate(BaseModel):
    description: str
    day: str
    time: str
    click_number: int

class ItemResponse(ItemCreate):
    id: int
    
    class Config:
        from_attributes = True

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинты
@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Эндпоинт для создания новой записи в базе данных.
    Принимает JSON с данными item (name, description, price).
    """
    db_item = ItemDB(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[ItemResponse])
def read_items(
    skip: int = Query(0, description="Количество записей для пропуска"),
    limit: int = Query(10, description="Количество записей на страницу"),
    db: Session = Depends(get_db)
):
    """
    Эндпоинт для получения списка записей из базы данных.
    Поддерживает пагинацию через параметры skip и limit.
    """
    items = db.query(ItemDB).offset(skip).limit(limit).all()
    return items