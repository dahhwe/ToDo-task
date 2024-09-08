from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base


class ToDo(Base):
    """
    Модель для элементов ToDo, хранящихся в базе данных.
    """
    __tablename__ = "todos"

    id: int = Column(Integer, primary_key=True, index=True)  # Идентификатор задачи
    title: str = Column(String, index=True)  # Название задачи
    description: str = Column(String, index=True)  # Описание задачи
    completed: bool = Column(Boolean, default=False)  # Статус выполнения задачи
    completion_date: Date = Column(Date, nullable=True)  # Дата завершения задачи
