from asyncpg import Connection

__all__ = [
    "FileService",
]


class FileService:
    _con: Connection

    def __init__(self, con: Connection) -> None:
        self._con = con

    async def create(self, user_id: int, path: str) -> int:
        query = "INSERT INTO processed_files(user_id, path) VALUES($1, $2) RETURNING ID"
        return await self._con.fetchval(query, user_id, path)
