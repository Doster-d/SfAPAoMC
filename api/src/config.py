import os

__all__ = [
    "PG_HOST",
    "PG_PORT",
    "PG_USER",
    "PG_PASS",
    "PG_DATABASE",
]

PG_HOST = os.getenv("DB_address", "127.0.0.1")
PG_PORT = os.getenv("DB_port", 6432)
PG_USER = os.getenv("DB_user", "patentexpertuser")
PG_PASS = os.getenv("DB_pass", "mycoolpassword123")
PG_DATABASE = os.getenv("DB_db", "patentanal")
