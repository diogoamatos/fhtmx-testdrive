from uuid import uuid4, UUID

from sqlmodel import SQLModel, Field


class TodoBase(SQLModel):
    text: str
    done: bool = False


class Todo(TodoBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)


class TodoPublic(TodoBase):
    id: UUID


class TodoCreate(TodoBase):
    text: str


class TodoUpdate(TodoBase):
    text: str
    done: bool = False
