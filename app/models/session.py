"""Application session persistence."""

import sqlite3
from datetime import datetime, timedelta, timezone


def create_session(
    connection: sqlite3.Connection, user_id: int, token_hash: str, lifetime_days: int
) -> None:
    expires_at = (datetime.now(timezone.utc) + timedelta(days=lifetime_days)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    with connection:
        connection.execute(
            "INSERT INTO sessions (user_id, token_hash, expires_at) VALUES (?, ?, ?)",
            (user_id, token_hash, expires_at),
        )


def delete_session(connection: sqlite3.Connection, token_hash: str) -> None:
    with connection:
        connection.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
