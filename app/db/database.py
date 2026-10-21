"""SQLite connection and schema initialization."""

import sqlite3
from collections.abc import Generator
from contextlib import closing

from app.core.config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    # FastAPI may resume a synchronous dependency's cleanup on a different
    # worker thread than the one that created the request-scoped connection.
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def get_db() -> Generator[sqlite3.Connection, None, None]:
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()


def initialize_database() -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                )"""
            )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    display_name TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                )"""
            )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS oauth_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    provider TEXT NOT NULL,
                    provider_user_id TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    UNIQUE(provider, provider_user_id)
                )"""
            )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS email_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
                    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                )"""
            )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    token_hash TEXT NOT NULL UNIQUE,
                    expires_at TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                )"""
            )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price INTEGER NOT NULL CHECK (price >= 0),
                    thumbnail_url TEXT,
                    instructor_name TEXT NOT NULL,
                    level TEXT NOT NULL,
                    duration INTEGER NOT NULL CHECK (duration >= 0),
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                )"""
            )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS payment_orders (
                    payment_id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    course_id INTEGER NOT NULL REFERENCES courses(id),
                    amount INTEGER NOT NULL CHECK (amount >= 0),
                    status TEXT NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'paid')),
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    paid_at TEXT
                )"""
            )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS course_enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    course_id INTEGER NOT NULL REFERENCES courses(id),
                    payment_id TEXT NOT NULL UNIQUE REFERENCES payment_orders(payment_id),
                    amount INTEGER NOT NULL CHECK (amount >= 0),
                    enrolled_at TEXT NOT NULL DEFAULT (datetime('now')),
                    UNIQUE(user_id, course_id)
                )"""
            )
            enrollment_columns = {
                row["name"] for row in connection.execute("PRAGMA table_info(course_enrollments)")
            }
            if "amount" not in enrollment_columns:
                connection.execute("ALTER TABLE course_enrollments ADD COLUMN amount INTEGER")
                connection.execute(
                    """UPDATE course_enrollments
                       SET amount = (SELECT amount FROM payment_orders
                                     WHERE payment_orders.payment_id = course_enrollments.payment_id)
                       WHERE amount IS NULL"""
                )
