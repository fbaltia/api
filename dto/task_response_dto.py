from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from models.task import Task


@dataclass
class TaskResponseDto:
    
    id: int
    name: str
    attribution_email: str
    start_date: datetime
    end_date: datetime
    status: Task.Status
    duration: int

    @classmethod
    def from_entity(cls: type[TaskResponseDto], task: Task) -> TaskResponseDto:
        return cls(
            # mapping
            id=task.id,
            name=task.name,
            status=task.status,
            start_date=task.start_date, 
            end_date=task.end_date,
            attribution_email=task.attribution_email, # modifier ici
            duration=(task.end_date - task.start_date).days,
        )
        