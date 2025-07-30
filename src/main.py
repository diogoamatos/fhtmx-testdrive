from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.todos.routes import todo_router
from src.routes import root_router
# from src.greet.routes import greet_router
# from src.heroes.routes import heroes_router

from .database import create_db_and_tables


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]


version = "v1"

app = FastAPI(
    # version=version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(todo_router, prefix="/todos", tags=['Todo'])
app.include_router(root_router, prefix="", tags=['Pages'])
# app.include_router(greet_router, prefix="/greet", tags=['Greet'])
# app.include_router(heroes_router, prefix="/hero", tags=['Heroes'])


@app.on_event("startup")
def on_startup():
    print("database create db and table on startup")
    create_db_and_tables()
