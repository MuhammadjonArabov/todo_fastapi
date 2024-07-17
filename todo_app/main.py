from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, database, models, schemas

models.Base.metadata.create_all(bind=database.sync_engine)

app = FastAPI(debug=True)


@app.post("/todos/", response_model=schemas.Todo)
async def create_todo(todo: schemas.TodoCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_todo(db=db, todo=todo)


@app.get("/todos/", response_model=List[schemas.Todo])
async def read_todos(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    todos = await crud.get_todo_list(db=db, skip=skip, limit=limit)
    return todos


@app.get("/todos/{todo_id}", response_model=schemas.Todo)
async def read_todo(todo_id: int, db: AsyncSession = Depends(database.get_db)):
    db_todo = await crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.put("/todos/{todo_id}", response_model=schemas.Todo)
async def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: AsyncSession = Depends(database.get_db)):
    db_todo = await crud.update_todo(db=db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.delete("/todos/{todo_id}", response_model=schemas.Todo)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(database.get_db)):
    db_todo = await crud.delete_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
