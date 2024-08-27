from fastapi import FastAPI, Depends, HTTPException, Request, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from deep_translator import GoogleTranslator

from todo_app import crud, database, schemas

app = FastAPI(debug=True)

# Global tilni saqlash
global_language = "en"


# Translator funktsiyasi
def translate_text(text: str, target_lang: str) -> str:
    translator = GoogleTranslator(source='auto', target=target_lang)
    return translator.translate(text)


@app.get("/set_language/")
async def set_language(lang: str):
    global global_language
    if lang in ["en", "ru", "uz"]:
        global_language = lang
        return {"message": f"Language set to {lang}"}
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")


@app.middleware("http")
async def set_locale_middleware(request: Request, call_next):
    # So'rovda til mavjudligini tekshirish
    request.state.lang = global_language  # Default tilni o'rnatish
    response = await call_next(request)
    return response


@app.post("/todos/", response_model=schemas.Todo)
async def create_todo(
        request: Request,
        todo: schemas.TodoCreate,
        db: AsyncSession = Depends(database.get_db)
):
    lang = getattr(request.state, 'lang', global_language)  # Default tilni olish
    translated_title = translate_text(todo.title, lang)
    translated_description = translate_text(todo.description, lang)
    todo.title = translated_title
    todo.description = translated_description
    return await crud.create_todo(db=db, todo=todo)


@app.get("/todos/", response_model=List[schemas.Todo])
async def read_todos(
        request: Request,
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(database.get_db)
):
    lang = getattr(request.state, 'lang', global_language)  # Default tilni olish
    todos = await crud.get_todo_list(db=db, skip=skip, limit=limit)
    for todo in todos:
        todo.title = translate_text(todo.title, lang)
        todo.description = translate_text(todo.description, lang)
    return todos


@app.get("/todos/{todo_id}", response_model=schemas.Todo)
async def read_todo(
        request: Request,
        todo_id: int,
        db: AsyncSession = Depends(database.get_db)
):
    lang = getattr(request.state, 'lang', global_language)  # Default tilni olish
    db_todo = await crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail=translate_text("Todo not found", lang))
    db_todo.title = translate_text(db_todo.title, lang)
    db_todo.description = translate_text(db_todo.description, lang)
    return db_todo


@app.put("/todos/{todo_id}", response_model=schemas.Todo)
async def update_todo(
        request: Request,
        todo_id: int,
        todo: schemas.TodoUpdate,
        db: AsyncSession = Depends(database.get_db)
):
    lang = getattr(request.state, 'lang', global_language)  # Default tilni olish
    db_todo = await crud.update_todo(db=db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail=translate_text("Todo not found", lang))
    db_todo.title = translate_text(db_todo.title, lang)
    db_todo.description = translate_text(db_todo.description, lang)
    return db_todo


@app.delete("/todos/{todo_id}", response_model=schemas.Todo)
async def delete_todo(
        request: Request,
        todo_id: int,
        db: AsyncSession = Depends(database.get_db)
):
    lang = getattr(request.state, 'lang', global_language)  # Default tilni olish
    db_todo = await crud.delete_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail=translate_text("Todo not found", lang))
    return db_todo
