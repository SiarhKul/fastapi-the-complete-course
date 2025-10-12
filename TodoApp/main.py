from http.client import HTTPException
from typing import Annotated
from pydantic import BaseModel, Field
from typing import Optional

from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends, Path
from starlette import status

from database import engine, SessionLocal
import models
from models import Todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    compted: bool


@app.get("/", status_code=200)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@app.get('/todo/{todo_id}', status_code=200)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')


@app.post('/todo', status_code=201)
async def create_todo(db: db_dependency,
                      todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()


@app.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)
                      ):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.compted = todo_request.compted

    db.add(todo_model)

    db.commit()
