"""Course listing and detail endpoints."""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_db
from app.models.course import get_course, list_courses
from app.schemas.course import (
    Course,
    CourseDetailResponse,
    CourseErrorResponse,
    CourseListResponse,
)

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=CourseListResponse)
def get_courses(connection: sqlite3.Connection = Depends(get_db)) -> CourseListResponse:
    try:
        courses = list_courses(connection)
    except sqlite3.Error as exc:
        raise HTTPException(status_code=500, detail="강의 목록을 조회하지 못했습니다.") from exc
    return CourseListResponse(
        code=200,
        message="강의 목록을 조회했습니다.",
        result=[Course(**course) for course in courses],
    )


@router.get(
    "/{course_id}",
    response_model=CourseDetailResponse,
    responses={404: {"model": CourseErrorResponse, "description": "강의를 찾을 수 없음"}},
)
def get_course_detail(
    course_id: int, connection: sqlite3.Connection = Depends(get_db)
) -> CourseDetailResponse:
    try:
        course = get_course(connection, course_id)
    except sqlite3.Error as exc:
        raise HTTPException(status_code=500, detail="강의 정보를 조회하지 못했습니다.") from exc
    if course is None:
        raise HTTPException(status_code=404, detail="강의를 찾을 수 없습니다.")
    return CourseDetailResponse(code=200, message="강의 상세 정보입니다.", result=Course(**course))
