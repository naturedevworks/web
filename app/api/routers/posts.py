"""Post endpoints."""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_db
from app.models.post import list_posts as fetch_posts
from app.schemas.common import ApiResponse
from app.schemas.post import Post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=ApiResponse)
def list_posts(connection: sqlite3.Connection = Depends(get_db)) -> ApiResponse:
    try:
        posts = fetch_posts(connection)
    except sqlite3.Error as exc:
        raise HTTPException(status_code=500, detail="게시글 목록을 조회하지 못했습니다.") from exc
    return ApiResponse(
        code=200,
        message="게시글 목록을 조회했습니다.",
        result=[Post(**post).dict() for post in posts],
    )
