"""PortOne V2 checkout, server-side payment confirmation, and enrollments."""

import json
import sqlite3
import urllib.error
import urllib.request
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import get_current_user, get_db
from app.core.config import PORTONE_API_SECRET, PORTONE_CHANNEL_KEY, PORTONE_STORE_ID
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/payments", tags=["payments"])


class CheckoutRequest(BaseModel):
    course_id: int


class ConfirmRequest(BaseModel):
    payment_id: str


def _require_user(user: dict[str, Any] | None) -> dict[str, Any]:
    if not user:
        raise HTTPException(status_code=401, detail="결제�?진행?�려�?로그?�해 주세??")
    return user


def _portone_payment(payment_id: str) -> dict[str, Any]:
    request = urllib.request.Request(
        f"https://api.portone.io/payments/{payment_id}",
        headers={"Authorization": f"PortOne {PORTONE_API_SECRET}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise HTTPException(status_code=502, detail="PortOne 결제 ?�역???�인?��? 못했?�니??") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=502, detail="PortOne 결제 ?�인 ?�비?�에 ?�결?��? 못했?�니??") from exc


@router.post("/checkout", response_model=ApiResponse)
def create_checkout(
    payload: CheckoutRequest,
    user=Depends(get_current_user),
    connection: sqlite3.Connection = Depends(get_db),
) -> ApiResponse:
    user = _require_user(user)
    if not (PORTONE_STORE_ID and PORTONE_CHANNEL_KEY and PORTONE_API_SECRET):
        raise HTTPException(status_code=503, detail="PortOne 결제 ?�정???�료?��? ?�았?�니??")

    course = connection.execute(
        "SELECT id, title, price FROM courses WHERE id = ?", (payload.course_id,)
    ).fetchone()
    if course is None:
        raise HTTPException(status_code=404, detail="강의�?찾을 ???�습?�다.")
    enrolled = connection.execute(
        "SELECT 1 FROM course_enrollments WHERE user_id = ? AND course_id = ?",
        (user["id"], payload.course_id),
    ).fetchone()
    if enrolled:
        raise HTTPException(status_code=409, detail="?��? 구매??강의?�니??")

    pending = connection.execute(
        """SELECT payment_id, amount FROM payment_orders
           WHERE user_id = ? AND course_id = ? AND status = 'pending'
           ORDER BY created_at DESC LIMIT 1""",
        (user["id"], course["id"]),
    ).fetchone()
    if pending:
        payment_id = pending["payment_id"]
        amount = pending["amount"]
    else:
        payment_id = f"course-{uuid.uuid4().hex}"
        amount = course["price"]
        connection.execute(
            "INSERT INTO payment_orders(payment_id, user_id, course_id, amount) VALUES (?, ?, ?, ?)",
            (payment_id, user["id"], course["id"], course["price"]),
        )
        connection.commit()
    return ApiResponse(
        code=200,
        message="결제 ?�청??준비했?�니??",
        result={
            "payment_id": payment_id,
            "course_id": course["id"],
            "order_name": course["title"],
            "amount": amount,
            "store_id": PORTONE_STORE_ID,
            "channel_key": PORTONE_CHANNEL_KEY,
        },
    )


@router.post("/confirm", response_model=ApiResponse)
def confirm_payment(
    payload: ConfirmRequest,
    user=Depends(get_current_user),
    connection: sqlite3.Connection = Depends(get_db),
) -> ApiResponse:
    user = _require_user(user)
    order = connection.execute(
        """SELECT payment_id, user_id, course_id, amount, status
           FROM payment_orders WHERE payment_id = ? AND user_id = ?""",
        (payload.payment_id, user["id"]),
    ).fetchone()
    if order is None:
        raise HTTPException(status_code=404, detail="결제 주문??찾을 ???�습?�다.")
    if order["status"] == "paid":
        return ApiResponse(code=200, message="?��? 결제가 ?�인?�었?�니??", result={"status": "PAID"})

    payment = _portone_payment(payload.payment_id)
    payment_amount = payment.get("amount")
    pg_total = payment_amount.get("total") if isinstance(payment_amount, dict) else None
    # PortOne returns the KRW total as an integer; reject missing or malformed values.
    if type(pg_total) is not int or pg_total != order["amount"]:
        raise HTTPException(status_code=400, detail="결제 금액??주문 금액�??�치?��? ?�습?�다.")
    if payment.get("status") != "PAID":
        raise HTTPException(status_code=409, detail="결제가 ?�직 ?�료?��? ?�았?�니??")

    try:
        with connection:
            connection.execute(
                "UPDATE payment_orders SET status = 'paid', paid_at = datetime('now') WHERE payment_id = ? AND status = 'pending'",
                (payload.payment_id,),
            )
            connection.execute(
                """INSERT OR IGNORE INTO course_enrollments
                   (user_id, course_id, payment_id, amount) VALUES (?, ?, ?, ?)""",
                (user["id"], order["course_id"], payload.payment_id, order["amount"]),
            )
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="강의 구매 ?�보�?반영?��? 못했?�니??") from exc
    return ApiResponse(code=200, message="결제가 ?�인?�어 강의 ?�강???�록?�었?�니??", result={"status": "PAID"})


@router.get("/enrollments", response_model=ApiResponse)
def list_enrollments(
    user=Depends(get_current_user),
    connection: sqlite3.Connection = Depends(get_db),
) -> ApiResponse:
    user = _require_user(user)
    rows = connection.execute(
        """SELECT c.id, c.title, c.description, c.price, c.thumbnail_url,
                  c.instructor_name, c.level, c.duration, e.enrolled_at
           FROM course_enrollments e
           JOIN courses c ON c.id = e.course_id
           JOIN payment_orders p ON p.payment_id = e.payment_id
           WHERE e.user_id = ? AND p.user_id = e.user_id AND p.course_id = e.course_id
             AND p.status = 'paid' AND p.amount = e.amount
           ORDER BY e.enrolled_at DESC, e.id DESC""",
        (user["id"],),
    ).fetchall()
    return ApiResponse(
        code=200,
        message="???�강 강의 목록??조회?�습?�다.",
        result=[dict(row) for row in rows],
    )


@router.get("/enrollments/{course_id}", response_model=ApiResponse)
def get_enrollment(
    course_id: int,
    user=Depends(get_current_user),
    connection: sqlite3.Connection = Depends(get_db),
) -> ApiResponse:
    user = _require_user(user)
    enrollment = connection.execute(
        """SELECT e.course_id, e.enrolled_at, c.title
           FROM course_enrollments e
           JOIN courses c ON c.id = e.course_id
           JOIN payment_orders p ON p.payment_id = e.payment_id
           WHERE e.user_id = ? AND e.course_id = ?
             AND p.user_id = e.user_id AND p.course_id = e.course_id
             AND p.status = 'paid' AND p.amount = e.amount""",
        (user["id"], course_id),
    ).fetchone()
    return ApiResponse(
        code=200,
        message="?�강 ?�록 ?�보�?조회?�습?�다.",
        result=dict(enrollment) if enrollment else None,
    )
