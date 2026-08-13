from pydantic import BaseModel, EmailStr, Field

from models.employee import Employee
from decimal import Decimal


class EmployeeRequestDto(BaseModel):
    last_name: str = Field()
    first_name: str = Field()
    email: EmailStr = Field()
    title: Employee.Title = Field()
    salary: Decimal = Field()
    supervisor_id: int|None = Field()