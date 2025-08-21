from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import ItemDB, ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse)
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

@router.get("/", response_model=List[ItemResponse])
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