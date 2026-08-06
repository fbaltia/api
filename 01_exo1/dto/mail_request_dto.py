from pydantic import BaseModel, EmailStr, Field


class MailRequestDto(BaseModel):
    subject: str = Field(default='No object', description='Sujet de l\'email')
    name: str = Field(description='Nom de l\'expéditeur')
    email: EmailStr = Field(description='Email de l\'expéditeur')
    content: str = Field(description='Contenu de l\'email')
