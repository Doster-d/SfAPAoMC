from typing import Annotated

from fastapi import Depends
from asyncpg import Connection

from src.database import get_db_connection

__all__ = [
    "FileService",
    "get_file_service",
]


class FileService:
    _con: Connection

    def __init__(self, con: Connection) -> None:
        self._con = con

    async def create(self, user_id: int, path: str) -> int:
        query = "INSERT INTO processed_files(user_id, path) VALUES($1, $2) RETURNING ID"
        return await self._con.fetchval(query, user_id, path)


def get_file_service(
    con: Connection = Depends(get_db_connection),
) -> FileService:
    return FileService(con)
