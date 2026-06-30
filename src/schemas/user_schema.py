from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr


class GameResult(str, Enum):
    win = "win"
    lose = "lose"
    draw = "draw"


class GameResultSchema(BaseModel):
    result: GameResult


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr

class UserStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    total_games: int
    total_wins: int
    total_loses: int
    total_draws: int


class UserStatsOut(BaseModel):
    user: UserStats


class UserOut(BaseModel):
    user: UserPublic

class UsersOut(BaseModel):
    users: list[UserPublic]

class TokenOut(BaseModel):
    token: str

class UserTokenOut(BaseModel):
    user: UserPublic
    token: str
