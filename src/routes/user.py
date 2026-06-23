from fastapi import APIRouter, HTTPException, Path, status, Security
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

from sqlalchemy.exc import SQLAlchemyError

from database.connection import get_engine
from database.models import User

from database.user_repository import *

from security.hash import hash_password, verify_password
from security.jwt import create_access_token, decode_access_token

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

user_router = APIRouter()

def token_payload(user: User) -> dict:
    return {"id": user.id, "name": user.name, "email": user.email}

@user_router.get("/all")
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

@user_router.get("")
def get_user(token: str = Security(oauth2_scheme)):
    current_user = decode_access_token(token)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user": current_user}

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
    token = create_access_token(token_payload(created_user))
    return {"user": created_user, "token": token}

@user_router.post("/login")
def login(credentials: LoginSchema):
    engine = get_engine()
    user = get_user_by_email_from_db(engine, credentials.email)
    if user is None or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
        )
    token = create_access_token(token_payload(user))
    return {"token": token}

@user_router.put("")
def update_user(user: UserSchema, token: str = Security(oauth2_scheme)):
    engine = get_engine()
    current_user = decode_access_token(token)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    new_data = User(
        id=current_user["id"],
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

@user_router.delete("")
def delete_user(token: str = Security(oauth2_scheme)):
    engine = get_engine()
    current_user = decode_access_token(token)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    existing_user = get_user_from_db(engine, current_user["id"])
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
