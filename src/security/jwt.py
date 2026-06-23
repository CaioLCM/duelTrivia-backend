import jwt

from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer

from core.settings import configs


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=configs.JWT_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, configs.JWT_SECRET, algorithm=configs.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token, configs.JWT_SECRET, algorithms=[configs.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        return None
