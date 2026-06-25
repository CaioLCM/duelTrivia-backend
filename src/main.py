from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.user import user_router
from src.routes.trivia import trivia_router
from src.routes.game import game_router

from src.database.models import Base
from src.database.connection import get_engine

from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError

import logging

@asynccontextmanager
async def lifespan(app):
    try:
        Base.metadata.create_all(bind=get_engine())
    except SQLAlchemyError:
        logging.warning("Banco indisponível: API subindo sem inicializar tabelas")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users", tags=["/users"])
app.include_router(trivia_router, prefix="/questions", tags=["/questions"])
app.include_router(game_router, prefix="/game", tags=["/game"])