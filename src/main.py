from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.user import user_router
from routes.trivia import trivia_router

from database.models import Base
from database.connection import get_engine

from contextlib import contextmanager

app = FastAPI()

@contextmanager
def lifespan(app):
    Base.metadata.create_all(bind=get_engine())
    yield

CORSMiddleware(
    app,
    allow_origins=()
)

app.include_router(user_router, prefix="/users")
app.include_router(trivia_router, prefix="/questions")