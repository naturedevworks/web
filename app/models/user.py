"""User persistence for social sign-in."""

import sqlite3
from typing import Any


def get_or_create_kakao_user(
    connection: sqlite3.Connection, kakao_user_id: str, nickname: str
) -> dict[str, Any]:
    with connection:
        row = connection.execute(
            """SELECT users.id, users.display_name
               FROM users JOIN oauth_accounts ON oauth_accounts.user_id = users.id
               WHERE oauth_accounts.provider = 'kakao'
                 AND oauth_accounts.provider_user_id = ?""",
            (kakao_user_id,),
        ).fetchone()
        if row:
            connection.execute(
                "UPDATE users SET display_name = ? WHERE id = ?",
                (nickname, row["id"]),
            )
            return {"id": row["id"], "nickname": nickname}

        cursor = connection.execute(
            "INSERT INTO users (display_name) VALUES (?)", (nickname,)
        )
        user_id = cursor.lastrowid
        connection.execute(
            """INSERT INTO oauth_accounts (user_id, provider, provider_user_id)
               VALUES (?, 'kakao', ?)""",
            (user_id, kakao_user_id),
        )
    return {"id": user_id, "nickname": nickname}


def create_email_user(
    connection: sqlite3.Connection,
    email: str,
    display_name: str,
    password_hash: str,
) -> dict[str, Any]:
    with connection:
        cursor = connection.execute(
            "INSERT INTO users (display_name) VALUES (?)", (display_name,)
        )
        user_id = cursor.lastrowid
        connection.execute(
            """INSERT INTO email_accounts (user_id, email, password_hash)
               VALUES (?, ?, ?)""",
            (user_id, email, password_hash),
        )
    return {"id": user_id, "nickname": display_name}


def get_email_user(
    connection: sqlite3.Connection, email: str
) -> dict[str, Any] | None:
    row = connection.execute(
        """SELECT users.id, users.display_name, email_accounts.password_hash
           FROM email_accounts JOIN users ON users.id = email_accounts.user_id
           WHERE email_accounts.email = ?""",
        (email,),
    ).fetchone()
    if not row:
        return None
    return {
        "id": row["id"],
        "nickname": row["display_name"],
        "password_hash": row["password_hash"],
    }


def get_user_by_session(
    connection: sqlite3.Connection, token_hash: str
) -> dict[str, Any] | None:
    row = connection.execute(
        """SELECT users.id, users.display_name
           FROM sessions JOIN users ON users.id = sessions.user_id
           WHERE sessions.token_hash = ? AND sessions.expires_at > CURRENT_TIMESTAMP""",
        (token_hash,),
    ).fetchone()
    if not row:
        return None
    return {"id": row["id"], "nickname": row["display_name"]}
