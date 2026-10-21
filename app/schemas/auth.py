"""Authentication request and response schemas."""

from pydantic import BaseModel, EmailStr, Field


class EmailRegistrationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class EmailLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class KakaoLoginRequest(BaseModel):
    code: str
    state: str


class UserSummary(BaseModel):
    id: int
    nickname: str
