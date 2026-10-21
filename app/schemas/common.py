"""Shared API response envelope."""

from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    code: int
    message: str
    result: Any = None
