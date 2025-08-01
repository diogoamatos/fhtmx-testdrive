from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine


DATABASE_URL = "sqlite:///sqlite.db"

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
