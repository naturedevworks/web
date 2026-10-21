"""Backend configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "app.db"
load_dotenv(BASE_DIR / ".env")

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY", "")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET", "")
KAKAO_REDIRECT_URI = os.getenv(
    "KAKAO_REDIRECT_URI", "http://localhost:5173/auth/kakao/callback"
)
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
COOKIE_SAMESITE = "none" if COOKIE_SECURE else "lax"
SESSION_DAYS = int(os.getenv("SESSION_DAYS", "30"))
_configured_frontend_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
FRONTEND_ORIGINS = list(
    dict.fromkeys(
        [
            *_configured_frontend_origins,
            "https://www.naturedevworks.kro.kr",
            "https://100.100.100.101",
        ]
    )
)

# Public PortOne V2 identifiers are returned to the authenticated checkout
# client. The API secret remains server-only and is never sent to the browser.
PORTONE_STORE_ID = os.getenv("PORTONE_STORE_ID", "")
PORTONE_CHANNEL_KEY = os.getenv("PORTONE_CHANNEL_KEY", "")
PORTONE_API_SECRET = os.getenv("PORTONE_API_SECRET", "")
