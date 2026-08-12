from sqlalchemy import select

from models.employee import Employee
from repositories.repository_base import RepositoryBase


class EmployeeRepository(RepositoryBase[Employee]):
    model = Employee

    def get_by_email(self, email: str) -> Employee|None:
        return self._session.scalars(
            select(Employee)
            .where(Employee.email.ilike(email))
        ).one_or_none()

    def get_hierarchy(self, id: int) -> list[Employee]:
        cte_r = (
            select(Employee).where(Employee.id == id)
            .cte(recursive=True)
        )
    
        recurse_stmt = (
            select(Employee)
            .join(cte_r, cte_r.c.supervisor_id == Employee.id)
        )
    
        stmt = select(cte_r.union_all(recurse_stmt))

        return list(self._session.scalars(select(Employee).from_statement(stmt)).all())