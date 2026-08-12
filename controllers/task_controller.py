from models.employee import Employee

from datetime import datetime, timedelta
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
)
from sqlalchemy import Sequence, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette.status import *

from dto.task_filter_request_dto import TaskFilterRequestDto
from dto.task_request_dto import TaskRequestDto
from dto.task_response_dto import TaskResponseDto
from models.base import get_session
from models.task import Task
from services.mailer import Mailer

router = APIRouter(prefix='/tasks', tags=['Tasks'])

@router.post('/', status_code=201)
async def create(
    background_tasks: BackgroundTasks,
    dto: Annotated[TaskRequestDto, Body()], 
    session: Annotated[Session, Depends(get_session)],
    mailer: Annotated[Mailer, Depends(Mailer)]
):
    empl = session.scalars(
        select(Employee)
        .where(Employee.email.ilike(dto.attribution_email))
    ).one_or_none()

    if not empl:
        raise HTTPException(HTTP_422_UNPROCESSABLE_CONTENT, 'Employé introuvable')
    if empl.title != Employee.Title.DEV:
        raise HTTPException(HTTP_422_UNPROCESSABLE_CONTENT, 'On ne peut attribué de tâches qu\'aux dev')

    task = Task()
    task.name = dto.name
    task.assign_to = empl
    task.end_date = datetime.now(tz=ZoneInfo('Europe/Paris')) + timedelta(days=dto.duration)
    session.add(task)
    # sauver en db sans commit
    session.flush()
    # emails = [empl.email]
    # e = empl
    # while e.supervisor:
    #     emails.append(e.supervisor.email)
    #     e = e.supervisor

    cte_r = (
        select(Employee).where(Employee.id == empl.id)
        .cte(recursive=True)
    )

    recurse_stmt = (
        select(Employee)
        .join(cte_r, cte_r.c.supervisor_id == Employee.id)
    )

    stmt = select(cte_r.union_all(recurse_stmt))

    result: list[Employee] = list(session.scalars(select(Employee).from_statement(stmt)).all())

    emails = [e.email for e in result]

    # envoyer l'email en arrière plan
    background_tasks.add_task(
        mailer.send_message,
        'Nouvelle tâche', emails,
        task.__dict__,
        'new_task.html'
    )
    return task.id

@router.get('/')
def get(
    dto: Annotated[TaskFilterRequestDto, Query()],
    session: Annotated[Session, Depends(get_session)]
) -> list[TaskResponseDto]:
    stmt = (select(Task)
        .offset((dto.page - 1) * dto.limit)
        .limit(dto.limit)
    )
    if dto.email:
        stmt.where(Task.attribution_email == dto.email)
    if dto.status:
        stmt.where(Task.status == dto.status)

    tasks = session.execute(stmt).scalars().all()
    # transforme chaque model db en dto
    return list(map(TaskResponseDto.from_entity, tasks))
    # return [TaskResponseDto.from_entity(t) for t in tasks]

@router.patch('/{id}')
def update_status(
    id: Annotated[int, Path()], 
    status: Annotated[Task.Status, Body(...)],
    session: Annotated[Session, Depends(get_session)],
):
    try:
        task = session.get_one(Task, id)
    except NoResultFound:
        raise HTTPException(HTTP_404_NOT_FOUND)
    
    if task.end_date < datetime.now(tz=ZoneInfo('Europe/Paris')):
        raise HTTPException(HTTP_422_UNPROCESSABLE_CONTENT, {
            'message': 'Il n\'est plus possible de modifier cet enregistrement'
        })

    task.status = status
    session.flush([task])
    return task.id

@router.delete('/{id}')
def delete(
    background_tasks: BackgroundTasks,
    id: Annotated[int, Path()], 
    session: Annotated[Session, Depends(get_session)],
    mailer: Annotated[Mailer, Depends(Mailer)]
):
    try:
        task: Task = session.get_one(Task, id)
    except NoResultFound:
        raise HTTPException(HTTP_404_NOT_FOUND)

    if task.status == Task.Status.done:
        raise HTTPException(HTTP_422_UNPROCESSABLE_CONTENT, {
            'message': 'Impossible de supprimer une tâche terminée'
        })

    background_tasks.add_task(
        mailer.send_message,
        'Tâche supprimée',
        [task.attribution_email], # modifier ici 
        task.__dict__,
        'task_removed.html'
    )
    session.delete(task)
    session.flush()
    return task.id

# @router.get('/e')
# def get_employee(sesssion: Session = Depends(get_session)):
#     stmt = (
#         select(Employee)
#         .options(joinedload(Employee.supervisor))
#         .where(Employee.id == 4)
#     )
#     e = sesssion.execute(stmt).scalars().one()
#     return {
#         e,
#         e.supervisor
#     }
#     # print(e.supervisor_id)
#     # print(e.supervisor.last_name)



    
