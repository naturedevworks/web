"""Common API dependencies."""

import sqlite3
from typing import Any

from fastapi import Cookie, Depends

from app.core.security import hash_token
from app.db.database import get_db
from app.models.user import get_user_by_session


def get_current_user(
    session_token: str | None = Cookie(default=None),
    connection: sqlite3.Connection = Depends(get_db),
) -> dict[str, Any] | None:
    if not session_token:
        return None
    return get_user_by_session(connection, hash_token(session_token))

__all__ = ["get_current_user", "get_db"]
