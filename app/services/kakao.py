"""Kakao authorization-code exchange and nickname lookup."""

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.core.config import (
    KAKAO_CLIENT_SECRET,
    KAKAO_REDIRECT_URI,
    KAKAO_REST_API_KEY,
)


class KakaoProviderError(Exception):
    """Raised when Kakao rejects a request or returns an invalid profile."""


def _request_json(
    url: str,
    data: dict[str, str] | None = None,
    token: str | None = None,
    operation: str = "카카오 API 요청",
) -> Any:
    headers = {"Accept": "application/json"}
    body = None
    if data is not None:
        body = urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded;charset=utf-8"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, data=body, headers=headers)
    try:
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        # Kakao returns useful OAuth error codes in the response body. Keep the
        # code, but omit error_description because it can contain the auth code.
        try:
            error_body = json.loads(exc.read().decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            error_body = {}
        error_code = error_body.get("error") if isinstance(error_body, dict) else None
        if error_code == "invalid_grant":
            detail = (
                "인가 코드가 거부되었습니다. 새 코드로 다시 시도하고, "
                "Kakao Redirect URI가 프런트엔드와 백엔드에서 "
                "http://localhost:5173/auth/kakao/callback 으로 같은지 확인하세요."
            )
        elif error_code == "invalid_client":
            detail = (
                "카카오 토큰 발급이 거부되었습니다. REST API 키가 현재 카카오 앱의 "
                "키인지, Client Secret 사용 설정과 값이 일치하는지 확인하세요."
            )
        elif error_code:
            detail = f"{operation} 실패 (Kakao {error_code})."
        else:
            detail = f"{operation} 실패 (HTTP {exc.code})."
        raise KakaoProviderError(detail) from exc
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        raise KakaoProviderError(f"{operation} 중 Kakao 서버와 통신하지 못했습니다.") from exc


def get_kakao_nickname(code: str) -> tuple[str, str]:
    if not KAKAO_REST_API_KEY:
        raise KakaoProviderError("카카오 REST API 키가 설정되지 않았습니다.")

    token_request = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_REST_API_KEY,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }
    if KAKAO_CLIENT_SECRET:
        token_request["client_secret"] = KAKAO_CLIENT_SECRET

    token_response = _request_json(
        "https://kauth.kakao.com/oauth/token",
        token_request,
        operation="카카오 토큰 발급",
    )
    if not isinstance(token_response, dict):
        raise KakaoProviderError("카카오 인증 응답 형식이 올바르지 않습니다.")
    access_token = token_response.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise KakaoProviderError("카카오 인증 응답에 액세스 토큰이 없습니다.")

    property_keys = json.dumps(["kakao_account.profile"], separators=(",", ":"))
    user_info = _request_json(
        "https://kapi.kakao.com/v2/user/me?"
        + urlencode({"property_keys": property_keys}),
        token=access_token,
        operation="카카오 프로필 조회",
    )
    if not isinstance(user_info, dict):
        raise KakaoProviderError("카카오 사용자 정보 응답 형식이 올바르지 않습니다.")
    kakao_user_id = user_info.get("id")
    account = user_info.get("kakao_account")
    profile = account.get("profile", {}) if isinstance(account, dict) else {}
    nickname = profile.get("nickname") if isinstance(profile, dict) else None
    if kakao_user_id is None or not isinstance(nickname, str) or not nickname.strip():
        raise KakaoProviderError("카카오에서 닉네임을 제공하지 않았습니다.")
    return str(kakao_user_id), nickname.strip()
