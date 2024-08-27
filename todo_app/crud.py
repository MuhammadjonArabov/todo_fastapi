from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from . import models, schemas


async def get_todo(db: AsyncSession, todo_id: int):
    result = await db.execute(select(models.Todo).filter(models.Todo.id == todo_id))
    return result.scalar_one_or_none()


async def get_todo_list(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Todo).offset(skip).limit(limit))
    return result.scalars().all()


async def create_todo(db: AsyncSession, todo: schemas.TodoCreate):
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
    )
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def update_todo(db: AsyncSession, todo_id: int, todo: schemas.TodoUpdate):
    db_todo = await get_todo(db=db, todo_id=todo_id)
    if db_todo:
        db_todo.status = todo.status
        db_todo.updated_at = func.now()
        await db.commit()
        await db.refresh(db_todo)
    return db_todo
