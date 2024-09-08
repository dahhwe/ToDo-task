from sqlalchemy.orm import Session
import models
import schemas
from typing import List, Optional


def get_todos(db: Session, skip: int = 0, limit: int = 10) -> List[models.ToDo]:
    """
    Получить список задач с возможностью пропуска и ограничения количества.

    :param db: Сессия базы данных.
    :param skip: Количество пропускаемых записей.
    :param limit: Максимальное количество возвращаемых записей.
    :return: Список задач.
    """
    return db.query(models.ToDo).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int) -> Optional[models.ToDo]:
    """
    Получить задачу по её идентификатору.

    :param db: Сессия базы данных.
    :param todo_id: Идентификатор задачи.
    :return: Задача или None, если задача не найдена.
    """
    return db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.ToDoCreate) -> models.ToDo:
    """
    Создать новую задачу.

    :param db: Сессия базы данных.
    :param todo: Данные для создания нов��й задачи.
    :return: Созданная задача.
    """
    db_todo: models.ToDo = models.ToDo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.ToDoUpdate) -> Optional[models.ToDo]:
    """
    Обновить существующую задачу.

    :param db: Сессия базы данных.
    :param todo_id: Идентификатор задачи.
    :param todo: Данные для обновления задачи.
    :return: Обновленная задача или None, если задача не найдена.
    """
    db_todo: Optional[models.ToDo] = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if db_todo:
        for key, value in todo.model_dump(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> Optional[models.ToDo]:
    """
    Удалить задачу по её идентификатору.

    :param db: Сессия базы данных.
    :param todo_id: Идентификатор задачи.
    :return: Удаленная задача или None, если задача не найдена.
    """
    db_todo: Optional[models.ToDo] = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
