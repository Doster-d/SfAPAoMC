from fastapi import Depends
from asyncpg import Connection

from src.database import get_db_connection

__all__ = [
    "UserService",
]


class UserService:
    _con: Connection

    def __init__(self, con: Connection) -> None:
        self._con = con

    async def create_user(self) -> None: ...

    async def fetch_by_id(self, user_id: str) -> None: ...


def get_user_service(con: Connection = Depends(get_db_connection)) -> UserService:
    return UserService(con)
