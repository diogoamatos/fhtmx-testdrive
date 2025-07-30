from fastapi import APIRouter, status, Query, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import select
from uuid import UUID

from typing import Annotated

from src.todos.models import Todo, TodoPublic, TodoCreate, TodoUpdate

from src.database import SessionDep

from src.config import templates


todo_router = APIRouter()



@todo_router.get("/", response_class=HTMLResponse)
async def todos_index(
    request: Request,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return templates.TemplateResponse(
        request=request, name="pages/todos.html", context={"todos": todos}
    )


@todo_router.get("/list", response_model=list[Todo])
async def todos_get_all(
    request: Request,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todos


@todo_router.post(
    "/create",
    response_model=TodoPublic,
    status_code=status.HTTP_201_CREATED,
)
async def todo_create(todo: TodoCreate, session: SessionDep):
    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@todo_router.get("/{todo_id}", response_model=TodoPublic)
async def todo_read(todo_id: UUID, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not Found",
        )
    return todo


@todo_router.patch("/{todo_id}", response_model=TodoPublic)
async def todo_update(todo_id: UUID, todo: TodoUpdate, session: SessionDep):
    todo_db = session.get(Todo, todo_id)
    if not todo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    todo_data = todo.model_dump(exclude_unset=True)
    todo_db.sqlmodel_update(todo_data)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return todo_db


@todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def todo_delete(todo_id: UUID, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    session.delete(todo)
    session.commit()
    return {"ok": True}
