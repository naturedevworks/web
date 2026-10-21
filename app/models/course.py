"""Course persistence queries."""

import sqlite3
from typing import Any


def list_courses(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = connection.execute(
        """SELECT id, title, description, price, thumbnail_url,
                  instructor_name, level, duration, created_at
           FROM courses ORDER BY id DESC"""
    ).fetchall()
    return [dict(row) for row in rows]


def get_course(connection: sqlite3.Connection, course_id: int) -> dict[str, Any] | None:
    row = connection.execute(
        """SELECT id, title, description, price, thumbnail_url,
                  instructor_name, level, duration, created_at
           FROM courses WHERE id = ?""",
        (course_id,),
    ).fetchone()
    return dict(row) if row is not None else None
