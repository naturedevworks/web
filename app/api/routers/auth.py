"""Kakao login, current-user, and logout endpoints."""

import logging
import secrets
import sqlite3

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response

from app.api.deps import get_current_user, get_db
from app.core.config import (
    COOKIE_SECURE,
    KAKAO_REDIRECT_URI,
    KAKAO_REST_API_KEY,
    SESSION_DAYS,
)
from app.core.security import create_token, hash_token
from app.models.session import create_session, delete_session
from app.models.user import get_or_create_kakao_user
from app.schemas.auth import KakaoLoginRequest
from app.schemas.common import ApiResponse
from app.services.kakao import KakaoProviderError, get_kakao_nickname

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)
STATE_COOKIE = "kakao_oauth_state"
SESSION_COOKIE = "session_token"
STATE_TTL_SECONDS = 600


@router.get("/kakao/state", response_model=ApiResponse)
def create_kakao_state(response: Response) -> ApiResponse:
    if not KAKAO_REST_API_KEY:
        raise HTTPException(status_code=503, detail="카카오 로그인이 설정되지 않았습니다.")
    state = create_token()
    response.set_cookie(
        STATE_COOKIE,
        state,
        max_age=STATE_TTL_SECONDS,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return ApiResponse(
        code=200,
        message="카카오 로그인 요청을 준비했습니다.",
        result={"state": state, "redirect_uri": KAKAO_REDIRECT_URI},
    )


@router.post("/kakao/login", response_model=ApiResponse)
def kakao_login(
    payload: KakaoLoginRequest,
    response: Response,
    state_cookie: str | None = Cookie(default=None, alias=STATE_COOKIE),
    connection: sqlite3.Connection = Depends(get_db),
) -> ApiResponse:
    if not state_cookie or not secrets.compare_digest(state_cookie, payload.state):
        raise HTTPException(status_code=400, detail="로그인 요청이 만료되었거나 올바르지 않습니다.")
    if not KAKAO_REST_API_KEY:
        raise HTTPException(status_code=503, detail="카카오 로그인이 설정되지 않았습니다.")

    try:
        kakao_user_id, nickname = get_kakao_nickname(payload.code)
    except KakaoProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    try:
        user = get_or_create_kakao_user(connection, kakao_user_id, nickname)
        session_token = create_token()
        create_session(connection, user["id"], hash_token(session_token), SESSION_DAYS)
    except sqlite3.Error as exc:
        logger.exception("Could not persist Kakao login to SQLite")
        raise HTTPException(
            status_code=500,
            detail="카카오 인증은 완료됐지만 로그인 정보를 DB에 저장하지 못했습니다. FastAPI 로그를 확인하세요.",
        ) from exc
    response.delete_cookie(STATE_COOKIE, path="/")
    response.set_cookie(
        SESSION_COOKIE,
        session_token,
        max_age=SESSION_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return ApiResponse(
        code=200,
        message="카카오 로그인에 성공했습니다.",
        result=user,
    )


@router.get("/me", response_model=ApiResponse)
def current_user(user=Depends(get_current_user)) -> ApiResponse:
    if not user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return ApiResponse(code=200, message="로그인 사용자 정보입니다.", result=user)


@router.post("/logout", response_model=ApiResponse)
def logout(
    response: Response,
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
    connection: sqlite3.Connection = Depends(get_db),
) -> ApiResponse:
    if session_token:
        delete_session(connection, hash_token(session_token))
    response.delete_cookie(SESSION_COOKIE, path="/")
    return ApiResponse(code=200, message="로그아웃했습니다.", result=None)
