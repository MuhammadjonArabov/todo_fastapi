from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from .database import Base
import enum


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Enum('pending', 'perform', 'completed', name="statustodo"), default='pending')
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
