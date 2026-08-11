from __future__ import annotations

from decimal import Decimal
from enum import StrEnum, auto
from typing import Optional

from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as SqlEnum, Numeric

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.task import Task

class Employee(Base):
    class Title(StrEnum):
        PM = auto()
        DEV = auto()

    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    salary: Mapped[Decimal] = mapped_column(Numeric(8,2), nullable=False)
    title: Mapped[Title] = mapped_column(SqlEnum(Title), nullable=False, default=Title.DEV)

    supervisor_id: Mapped[Optional[int]] = mapped_column(ForeignKey('employees.id'), nullable=True)
    supervisor: Mapped[Optional[Employee]] = relationship(remote_side=[id])
    # supervisor: Mapped[Optional[Employee]] = relationship(back_populates='subordinates', remote_side=[id])
    subordinates: Mapped[list[Employee]] = relationship(back_populates='supervisor')

    tasks: Mapped[list[Task]] = relationship(back_populates='assign_to')
