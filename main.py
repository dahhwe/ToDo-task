from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.requests import Request

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db() -> Session:
    """
    Получить сессию базы данных.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request) -> HTMLResponse:
    """
    Отобразить главную страницу.

    :param request: Запрос.
    :return: HTML-ответ с главной страницей.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/todos/", response_model=schemas.ToDo)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)) -> schemas.ToDo:
    """
    Создать новую задачу.

    :param todo: Данные для создания новой задачи.
    :param db: Сессия базы данных.
    :return: Созданная задача.
    """
    return crud.create_todo(db=db, todo=todo)


@app.get("/todos/", response_model=list[schemas.ToDo])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[schemas.ToDo]:
    """
    Получить список задач с возможностью пропуска и ограничения количества.

    :param skip: Количество пропускаемых записей.
    :param limit: Максимальное количество возвращаемых записей.
    :param db: Сессия базы данных.
    :return: Список задач.
    """
    return crud.get_todos(db, skip=skip, limit=limit)


@app.get("/todos/{todo_id}", response_model=schemas.ToDo)
def read_todo(todo_id: int, db: Session = Depends(get_db)) -> schemas.ToDo:
    """
    Получить задачу по её идентификатору.

    :param todo_id: Идентификатор задачи.
    :param db: Сессия базы данных.
    :return: Задача или None, если задача не найдена.
    """
    db_todo: schemas.ToDo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return db_todo


@app.put("/todos/{todo_id}", response_model=schemas.ToDo)
def update_todo(todo_id: int, todo: schemas.ToDoUpdate, db: Session = Depends(get_db)) -> schemas.ToDo:
    """
    Обновить существующую задачу.

    :param todo_id: Идентификатор задачи.
    :param todo: Данные для обновления задачи.
    :param db: Сессия базы данных.
    :return: Обновленная задача или None, если задача не найдена.
    """
    db_todo: schemas.ToDo = crud.update_todo(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return db_todo


@app.delete("/todos/{todo_id}", response_model=schemas.ToDo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> schemas.ToDo:
    """
    Удалить задачу по её идентификатору.

    :param todo_id: Идентификатор задачи.
    :param db: Сессия базы данных.
    :return: Удаленная задача или None, если задача не найдена.
    """
    db_todo: schemas.ToDo = crud.delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return db_todo
