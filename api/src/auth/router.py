from fastapi import Depends, HTTPException, status, APIRouter, JSONResponse
from pydantic import BaseModel

__all__ = [
    "router",
]

router = APIRouter()


class CreateUserScheme(BaseModel):
    username: str
    email: str
    password: str


class LoginUserScheme(BaseModel):
    email: str
    username: str


class LoginUserResult(BaseModel):
    userId: int
    accessToken: str
    username: str


@router.post("/signup")
def create_user(user: CreateUserScheme) -> LoginUserResult: ...


@router.post("/signin")
def login_user(user: LoginUserScheme) -> JSONResponse: ...
