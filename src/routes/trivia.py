from fastapi import APIRouter, HTTPException, status, Security

import httpx

from src.security.jwt import decode_access_token, oauth2_scheme

trivia_router = APIRouter()

@trivia_router.get("")
def get_questions(token: str = Security(oauth2_scheme)):
    current_user = decode_access_token(token)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        response = httpx.get("https://opentdb.com/api.php?amount=10")
        response.raise_for_status()
    except:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erro ao buscar questões"
        )
    data = response.json()
    return {"questions": data["results"]}