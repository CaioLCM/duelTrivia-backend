from fastapi import APIRouter, Path

from typing import Annotated

user_router = APIRouter()

@user_router.get("/users")
def get_users():
    pass

@user_router.get("/users/{user_id}")
def get_user(user_id: Annotated[int, Path(title="ID do usuário a ser buscado")]):
    pass

@user_router.post("/users")
def create_user():
    pass

@user_router.put("/users/{user_id}")
def update_user(user_id: Annotated[int, Path(title="ID do usuário a ser atualizado")]):
    pass

@user_router.delete("/users/{user_id}")
def delete_user(user_id: Annotated[int, Path(title="ID do usuário a ser removido")]):
    pass

