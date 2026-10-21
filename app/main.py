"""FastAPI application and shared response handling."""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routers.posts import router as posts_router
from app.api.routers.courses import router as courses_router
from app.api.routers.auth import router as auth_router
from app.api.routers.payments import router as payments_router
from app.core.config import FRONTEND_ORIGINS
from app.db.database import initialize_database

app = FastAPI(title="온라인 강의 API")
logger = logging.getLogger(__name__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)
app.include_router(posts_router)
app.include_router(courses_router)
app.include_router(auth_router)
app.include_router(payments_router)


def _envelope(code: int, message: str, result: Any = None) -> dict[str, Any]:
    return {"code": code, "message": message, "result": result}


@app.on_event("startup")
def startup() -> None:
    initialize_database()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "요청을 처리하지 못했습니다."
    return JSONResponse(
        status_code=exc.status_code,
        content=_envelope(exc.status_code, message),
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            _envelope(
                422,
                "요청 값이 올바르지 않습니다.",
                [
                    {
                        "loc": error["loc"],
                        "msg": error["msg"],
                        "type": error["type"],
                    }
                    for error in exc.errors()
                ],
            )
        ),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    # Keep the client response generic, but make the real cause visible in the
    # Uvicorn console so a production 500 can be diagnosed from the server log.
    logger.error(
        "Unhandled error while handling %s %s",
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=500,
        content=_envelope(500, "서버 내부 오류가 발생했습니다."),
    )
