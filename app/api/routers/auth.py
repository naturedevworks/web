"""Kakao login, current-user, and logout endpoints."""

import logging
import secrets
import sqlite3

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response

from app.api.deps import get_current_user, get_db
from app.core.passwords import DUMMY_PASSWORD_HASH, hash_password, verify_password
from app.core.config import (
    COOKIE_SECURE,
    COOKIE_SAMESITE,
    KAKAO_REDIRECT_URI,
    KAKAO_REST_API_KEY,
    SESSION_DAYS,
)
from app.core.security import create_token, hash_token
from app.models.session import create_session, delete_session
from app.models.user import create_email_user, get_email_user, get_or_create_kakao_user
from app.schemas.auth import (
    EmailLoginRequest,
    EmailRegistrationRequest,
    KakaoLoginRequest,
)
from app.schemas.common import ApiResponse
from app.services.kakao import KakaoProviderError, get_kakao_nickname

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)
STATE_COOKIE = "kakao_oauth_state"
SESSION_COOKIE = "session_token"
STATE_TTL_SECONDS = 600


def clear_auth_cookie(response: Response, name: str) -> None:
    # Keep the auth cookie scoped to the API host that issued it.
    response.delete_cookie(
        name,
        path="/",
        secure=COOKIE_SECURE,
        httponly=True,
        samesite=COOKIE_SAMESITE,
    )


def start_user_session(
    response: Response, connection: sqlite3.Connection, user_id: int
) -> None:
    session_token = create_token()
    create_session(connection, user_id, hash_token(session_token), SESSION_DAYS)
    clear_auth_cookie(response, SESSION_COOKIE)
    response.set_cookie(
        SESSION_COOKIE,
        session_token,
        max_age=SESSION_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        path="/",
    )


@router.get("/kakao/state", response_model=ApiResponse)
def create_kakao_state(response: Response) -> ApiResponse:
    if not KAKAO_REST_API_KEY:
        raise HTTPException(status_code=503, detail="카카오 로그인이 설정되지 않았습니다.")
    state = create_token()
    clear_auth_cookie(response, STATE_COOKIE)
    response.set_cookie(
        STATE_COOKIE,
        state,
        max_age=STATE_TTL_SECONDS,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
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
        start_user_session(response, connection, user["id"])
    except sqlite3.Error as exc:
        logger.exception("Could not persist Kakao login to SQLite")
        raise HTTPException(
            status_code=500,
            detail="카카오 인증은 완료됐지만 로그인 정보를 DB에 저장하지 못했습니다. FastAPI 로그를 확인하세요.",
        ) from exc
    clear_auth_cookie(response, STATE_COOKIE)
    return ApiResponse(
        code=200,
        message="카카오 로그인에 성공했습니다.",
        result=user,
    )


@router.post("/email/register", response_model=ApiResponse)
def register_email(
    payload: EmailRegistrationRequest,
    response: Response,
    connection: sqlite3.Connection = Depends(get_db),
) -> ApiResponse:
    display_name = payload.name.strip()
    if not display_name:
        raise HTTPException(status_code=422, detail="이름을 입력해 주세요.")

    email = str(payload.email).strip().casefold()
    try:
        user = create_email_user(
            connection,
            email,
            display_name,
            hash_password(payload.password),
        )
        start_user_session(response, connection, user["id"])
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="이미 가입된 이메일입니다.") from exc
    except sqlite3.Error as exc:
        logger.exception("Could not persist email account registration")
        raise HTTPException(
            status_code=500, detail="회원가입 정보를 저장하지 못했습니다."
        ) from exc

    return ApiResponse(code=200, message="회원가입이 완료되었습니다.", result=user)


@router.post("/email/login", response_model=ApiResponse)
def login_email(
    payload: EmailLoginRequest,
    response: Response,
    connection: sqlite3.Connection = Depends(get_db),
) -> ApiResponse:
    email = str(payload.email).strip().casefold()
    user = get_email_user(connection, email)
    encoded_hash = user["password_hash"] if user else DUMMY_PASSWORD_HASH
    if not verify_password(payload.password, encoded_hash) or not user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    try:
        start_user_session(response, connection, user["id"])
    except sqlite3.Error as exc:
        logger.exception("Could not create an email login session")
        raise HTTPException(
            status_code=500, detail="로그인 정보를 저장하지 못했습니다."
        ) from exc

    return ApiResponse(
        code=200,
        message="로그인에 성공했습니다.",
        result={"id": user["id"], "nickname": user["nickname"]},
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
    clear_auth_cookie(response, SESSION_COOKIE)
    return ApiResponse(code=200, message="로그아웃했습니다.", result=None)
