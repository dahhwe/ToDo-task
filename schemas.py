from datetime import date
from typing import Optional

from pydantic import BaseModel


class ToDoBase(BaseModel):
    """Базовая модель для элементов ToDo."""
    title: str  # Название задачи
    description: str  # Описание задачи
    completion_date: date  # Дата завершения задачи


class ToDoCreate(ToDoBase):
    """Модель для создания новой задачи ToDo."""
    pass


class ToDoUpdate(ToDoBase):
    """Модель для обновления существующей задачи ToDo."""
    title: Optional[str] = None  # Название задачи
    description: Optional[str] = None  # Описание задачи
    completion_date: Optional[date] = None  # Дата завершения задачи
    completed: Optional[bool] = None  # Статус выполнения задачи


class ToDoInDBBase(ToDoBase):
    """Базовая модель для элементов ToDo, хранящихся в базе данных."""
    id: int  # Идентификатор задачи
    completed: bool  # Статус выполнения задачи

    class Config:
        from_attributes = True


class ToDo(ToDoInDBBase):
    """Модель для элементов ToDo, возвращаемых из API."""
    pass
