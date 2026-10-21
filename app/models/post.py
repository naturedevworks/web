"""Post persistence queries."""

import sqlite3
from typing import Any


def list_posts(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = connection.execute(
        "SELECT id, title, content, created_at FROM posts ORDER BY id DESC"
    ).fetchall()
    return [dict(row) for row in rows]
