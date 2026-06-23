import bcrypt

from fastapi import APIRouter, HTTPException, Path, status

from typing import Annotated

from sqlalchemy.exc import SQLAlchemyError

from database.connection import get_engine
from database.models import User

from database.user_repository import *

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

user_router = APIRouter()

@user_router.get("")
def get_users():
    engine = get_engine()
    try:
        users = get_users_from_db(engine)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar os usuários",
        )
    return {"users": users}

@user_router.get("/{user_id}")
def get_user(user_id: Annotated[int, Path(title="ID do usuário a ser buscado")]):
    engine = get_engine()
    user = get_user_from_db(engine, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    return {"user": user}

@user_router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    engine = get_engine()
    new_user = User(
        name=user.name, email=user.email, password=hash_password(user.password)
    )
    try:
        created_user = add_user_at_db(engine, new_user)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível criar o usuário",
        )
    return {"user": created_user}

@user_router.post("/login")
def login(credentials: LoginSchema):
    engine = get_engine()
    user = get_user_by_email_from_db(engine, credentials.email)
    if user is None or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
        )
    return {"user": user}

@user_router.put("/{user_id}")
def update_user(
    user_id: Annotated[int, Path(title="ID do usuário a ser atualizado")],
    user: UserSchema,
):
    engine = get_engine()
    if get_user_from_db(engine, user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    new_data = User(
        id=user_id,
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
    )
    try:
        updated_user = update_user_at_db(engine, new_data)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar o usuário",
        )
    return {"user": updated_user}

@user_router.delete("/{user_id}")
def delete_user(user_id: Annotated[int, Path(title="ID do usuário a ser removido")]):
    engine = get_engine()
    existing_user = get_user_from_db(engine, user_id)
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    try:
        deleted_user = delete_user_at_db(engine, existing_user)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível remover o usuário",
        )
    return {"user": deleted_user}
