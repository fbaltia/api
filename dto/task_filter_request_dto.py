from pydantic import BaseModel, EmailStr, Field

from models.task import Task


class TaskFilterRequestDto(BaseModel):
    email: EmailStr | None = Field(default=None)
    status: Task.Status | None = Field(default=None)
    limit: int = Field(default=10, gt=0, le=100)
    page: int = Field(default=1, gt=0)