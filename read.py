from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Base, Todo
from database import engine, SessionLocal
from typing import Annotated

app = FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/read_all")
async def read_all(db: db_dependency):
    todos = db.query(Todo).all()
    return [todo.__dict__ for todo in todos]
