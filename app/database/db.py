import sqlite3
from pathlib import Path

from app.database.schema import create_schema
from app.database.seed import ensure_seed_data

DB_FILENAME = "db.sqlite3"
_connection: sqlite3.Connection | None = None


def _database_path() -> Path:
    project_root = Path(__file__).resolve().parents[2]
    return project_root / DB_FILENAME


def get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(_database_path())
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA foreign_keys = ON;")
    return _connection


def init_database() -> None:
    connection = get_connection()
    create_schema(connection)
    ensure_seed_data(connection)


def close_connection() -> None:
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None
