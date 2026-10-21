"""Authentication request and response schemas."""

from pydantic import BaseModel


class KakaoLoginRequest(BaseModel):
    code: str
    state: str


class UserSummary(BaseModel):
    id: int
    nickname: str
