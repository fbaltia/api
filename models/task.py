from __future__ import annotations

from datetime import datetime
from enum import StrEnum, auto
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.employee import Employee

class Task(Base):
    class Status(StrEnum):
        in_progress = auto()
        done = auto()
        
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(SqlEnum(Status), nullable=False, default=Status.in_progress)
    start_date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    end_date: Mapped[datetime] = mapped_column(nullable=False)

    assign_to_id: Mapped[int] = mapped_column(ForeignKey('employees.id'), nullable=False)
    assign_to: Mapped[Employee] = relationship(back_populates='tasks')