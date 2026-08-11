
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
from sqlalchemy import select
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
    task = Task()
    task.name = dto.name
    # modifier ici
    task.attribution_email = dto.attribution_email
    task.end_date = datetime.now(tz=ZoneInfo('Europe/Paris')) + timedelta(days=dto.duration)
    session.add(task)
    # sauver en db sans commit
    session.flush()
    # envoyer l'email en arrière plan
    background_tasks.add_task(
        mailer.send_message,
        'Nouvelle tâche', [task.attribution_email],
        task.__dict__,
        'new_task.html'
    )
    return task.id

@router.get('/')
def get(
    dto: Annotated[TaskFilterRequestDto, Query()],
    session: Annotated[Session, Depends(get_session)]
) -> map[TaskResponseDto]:
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
    return map(TaskResponseDto.from_entity, tasks)
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



    
