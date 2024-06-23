from fastapi import Depends
from asyncpg import Connection

from src.database import get_db_connection
from src.dto import ProcessedFile

__all__ = [
    "FileService",
    "get_file_service",
]


class FileService:
    _con: Connection

    def __init__(self, con: Connection) -> None:
        self._con = con

    async def create(
            self,
            user_id: int,
            path: str,
            file_type: str,
            patent_type=None,
            classification_json="{}"
    ) -> int:
        query = """
        INSERT INTO processed_files(user_id, path, file_type, patent_type, patent_classification_json)
        VALUES($1, $2, $3, $4, $5)
        RETURNING ID
        """
        return await self._con.fetchval(query, user_id, path, file_type, patent_type,
                                        classification_json)

    async def fetch_by_id(self, file_id: int) -> ProcessedFile | None:
        query = "SELECT * FROM processed_files WHERE id=$1"

        result = await self._con.fetchrow(query, file_id)

        if result is None:
            return None

        return ProcessedFile(**result)


def get_file_service(
    con: Connection = Depends(get_db_connection),
) -> FileService:
    return FileService(con)
