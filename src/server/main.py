from fastapi import FastAPI
from .database import engine, Base
from .routers import items

# Инициализация FastAPI
app = FastAPI()

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Подключение роутеров
app.include_router(items.router)

@app.get("/")
def read_root():
    return {"message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)