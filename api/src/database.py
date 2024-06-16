from typing import AsyncGenerator
from asyncpg import connect, Connection

from .config import PG_HOST, PG_PORT, PG_USER, PG_DATABASE, PG_PASS

__all__ = [
    "get_db_connection",
]


async def get_db_connection() -> AsyncGenerator[Connection, None]:
    con = await connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, database=PG_DATABASE, password=PG_PASS
    )
    yield con
    await con.close()
