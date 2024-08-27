from datetime import datetime

from pydantic import BaseModel, validator
from enum import Enum
from fastapi import HTTPException


class StatusTodo(str, Enum):
    PENDING = 'pending'
    PERFORM = 'perform'
    COMPLETED = 'completed'


class TodoBase(BaseModel):
    title: str
    description: str


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    status: str

    @validator('status')
    @classmethod
    def validate_status(cls, value):
        if value not in ['pending', 'perform', 'completed']:
            raise HTTPException(
                status_code=400,
                detail={
                    'status': 'Bunday status mavjud emas'
                }
            )
        return value


class TodoInDBBase(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Todo(TodoInDBBase):
    pass
