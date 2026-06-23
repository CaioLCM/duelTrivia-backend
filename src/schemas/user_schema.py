from pydantic import BaseModel, ConfigDict, EmailStr


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

class UserOut(BaseModel):
    user: UserPublic

class UsersOut(BaseModel):
    users: list[UserPublic]

class TokenOut(BaseModel):
    token: str

class UserTokenOut(BaseModel):
    user: UserPublic
    token: str
