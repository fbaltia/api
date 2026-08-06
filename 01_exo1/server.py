from pathlib import Path

from fastapi import Body, FastAPI, Query
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
import uvicorn
from dotenv import load_dotenv
import os

from dto.hello_request_dto import HelloRequestDto
from dto.hello_response_dto import HelloResponseDto
from dto.mail_request_dto import MailRequestDto

load_dotenv()

# créer une instance de FastAPI
app = FastAPI()

@app.get('/hello')
def hello(
    # name: str = Query(default='Khun', description='Permet de définir qui sera saluer'), 
    # nb: int = Query(default=1, description='Permet de définir combien de fois')
    dto: HelloRequestDto = Query()
) -> HelloResponseDto:
    """
    Fonction test qui permet de dire bonjour !
    """
    return HelloResponseDto(
        result=f'Hello {dto.name * dto.nb}',
        square=dto.nb**2
    )
    # return { 'result': f'Hello {dto.name * dto.nb}', 'square': dto.nb**2 }

@app.post('/mail', status_code=201)
async def mail(dto: MailRequestDto = Body()) -> None:
    config = ConnectionConfig(
        MAIL_SERVER=os.getenv('SMTP_HOST'),
        MAIL_PORT=int(os.getenv('SMTP_PORT')),
        MAIL_USERNAME=os.getenv('SMTP_USER'),
        MAIL_PASSWORD=os.getenv('SMTP_PASS'),
        MAIL_SSL_TLS=False,
        MAIL_STARTTLS=False,
        MAIL_FROM='admin@admin.be',
        TEMPLATE_FOLDER = Path(__file__).parent / 'templates'
    )
    message = MessageSchema(
        subject=dto.subject,
        from_email='admin@admin.be',
        reply_to=[dto.email],
        recipients=['lykhun@gmail.com'],
        template_body=dto.__dict__,
        # body=f'L\'utilisateur {dto.name} ({dto.email}): Ce mail contenait: {dto.content}',
        subtype='html'
    )
    mailer = FastMail(config)
    await mailer.send_message(message, template_name='mail_template.html')

if __name__ == '__main__':
    # exposer FastAPI sur le port 8000
    uvicorn.run(
        'server:app', 
        host='127.0.0.1',
        port=8000,
        reload=True
    )
