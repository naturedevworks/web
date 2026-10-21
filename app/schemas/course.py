"""Course response schemas."""

from pydantic import BaseModel, ConfigDict


class Course(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    price: int
    thumbnail_url: str | None
    instructor_name: str
    level: str
    duration: int
    created_at: str


class CourseListResponse(BaseModel):
    code: int
    message: str
    result: list[Course]


class CourseDetailResponse(BaseModel):
    code: int
    message: str
    result: Course


class CourseErrorResponse(BaseModel):
    code: int
    message: str
    result: None = None
