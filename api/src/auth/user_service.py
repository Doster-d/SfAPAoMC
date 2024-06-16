from fastapi import Depends
from asyncpg import Connection
from passlib.context import CryptContext
from uuid import uuid4

from src.database import get_db_connection
from src.dto import User, Token
from .schemas import CreateUserScheme

__all__ = [
    "UserService",
    "get_user_service",
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    _con: Connection

    def __init__(self, con: Connection) -> None:
        self._con = con

    async def create_user(self, data: CreateUserScheme) -> None:
        query = (
            "INSERT INTO users (username, email, hashed_password) VALUES($1, $2, $3)"
        )

        await self._con.execute(
            query, data.username, data.email, pwd_context.hash(data.password)
        )

    def verify_password(self, user: User, password: str) -> bool:
        return pwd_context.verify(password, user.hashed_password)

    async def fetch_by_id(self, user_id: int) -> User | None:
        query = "SELECT * FROM users WHERE id=$1"
        result = await self._con.fetchrow(query, user_id)

        if result is None:
            return None

        return User(**result)

    async def fetch_by_email(self, email: str) -> User | None:
        query = "SELECT * FROM users WHERE email LIKE $1"
        result = await self._con.fetchrow(query, email)

        if result is None:
            return None

        return User(**result)

    async def fetch_by_token(self, token: str) -> User | None:
        query = "SELECT * from access_tokens WHERE token LIKE $1"

        result = await self._con.fetchrow(query, token)

        if result is None:
            return None

        return await self.fetch_by_id(result["user_id"])

    async def create_access_token(self, user: User) -> str:
        token = str(uuid4())
        query = "INSERT INTO access_tokens (token, user_id) VALUES($1, $2)"
        await self._con.execute(query, token, user.id)

        return token


def get_user_service(con: Connection = Depends(get_db_connection)) -> UserService:
    return UserService(con)
