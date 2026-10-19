"""FastAPI application exposing the post list endpoint."""

import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


DATABASE_PATH = Path(__file__).resolve().parent / "app.db"
app = FastAPI(title="게시글 API")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )"""
        )


@app.on_event("startup")
def startup() -> None:
    initialize_database()


def envelope(code: int, message: str, result: Any) -> dict[str, Any]:
    return {"code": code, "message": message, "result": result}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=envelope(exc.status_code, str(exc.detail), None),
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            envelope(422, "요청 값이 올바르지 않습니다.", exc.errors())
        ),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=envelope(500, "서버 내부 오류가 발생했습니다.", None),
    )


@app.get("/posts")
def list_posts() -> dict[str, Any]:
    """Return posts in newest-first order."""
    try:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT id, title, content, created_at FROM posts ORDER BY id DESC"
            ).fetchall()
    except sqlite3.Error as exc:
        raise HTTPException(status_code=500, detail="게시글을 조회하지 못했습니다.") from exc

    posts = [dict(row) for row in rows]
    return envelope(200, "게시글 목록을 조회했습니다.", posts)
