import asyncio
import json
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import StreamingResponse

from dto.hello_request_dto import HelloRequestDto
from dto.hello_response_dto import HelloResponseDto
from dto.mail_request_dto import MailRequestDto
from services.mailer import Mailer

router = APIRouter(prefix='/default', tags=['Default'])

@router.get('/hello/{id}')
def hello(
    # name: str = Query(default='Khun', description='Permet de définir qui sera saluer'), 
    # nb: int = Query(default=1, description='Permet de définir combien de fois')
    dto: Annotated[HelloRequestDto, Query()],
    id: Annotated[int, Path()]
) -> HelloResponseDto:
    """
    Fonction test qui permet de dire bonjour !
    """
    print('id', id)
    return HelloResponseDto(
        result=f'Hello {dto.name * dto.nb}',
        square=dto.nb**2,
    )
    # return { 'result': f'Hello {dto.name * dto.nb}', 'square': dto.nb**2 }


@router.post('/mail', status_code=201)
async def mail(
    dto: Annotated[MailRequestDto, Body()],
    mailer: Annotated[Mailer, Depends(Mailer)]
) -> None:
    await mailer.send_message(
        dto.subject,
        dest=['lykhun@gmail.com'],
        template_body=dto.__dict__,
        template_name='mail_template.html'
    )

async def generate_flow():
    yield json.dumps({ 'value': 'Coucou' }) + '\n'
    await asyncio.sleep(2)
    yield json.dumps({ 'value': 'Coucou, Comment ' }) + '\n'
    await asyncio.sleep(2)
    yield json.dumps({ 'value': 'Coucou, Comment ca' }) + '\n'
    await asyncio.sleep(2)
    yield json.dumps({ 'value': 'Coucou, Comment ca?' }) + '\n'

@router.get('/stream')
def get_stream():
    return StreamingResponse(
        content=generate_flow(),
        media_type='application/x-ndjson'
    )
