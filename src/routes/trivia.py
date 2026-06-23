from fastapi import APIRouter, HTTPException, status

import httpx

trivia_router = APIRouter()

@trivia_router.get("/")
def get_questions():
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