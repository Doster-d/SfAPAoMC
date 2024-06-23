from pydantic import BaseModel

__all__ = [
    "CreateUserScheme",
    "LoginUserScheme",
    "LoginUserResult",
]


class CreateUserScheme(BaseModel):
    username: str
    email: str
    password: str


class LoginUserScheme(BaseModel):
    email: str
    password: str


class LoginUserResult(BaseModel):
    userId: int
    accessToken: str
    username: str
    email: str
