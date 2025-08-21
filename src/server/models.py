from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from .database import Base

# Pydantic модели для валидации
class ItemCreate(BaseModel):
    description: str
    day: str
    time: str
    click_number: int

# Pydantic модель для ответа
class ItemResponse(ItemCreate):
    id: int
    
    class Config:
        from_attributes = True

# Модель для базы данных
class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    day = Column(String)
    time = Column(String)
    click_number = Column(Integer)