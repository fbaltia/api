from pydantic import BaseModel, Field


class HelloRequestDto(BaseModel):
    name: str = Field(description='Qui sera saluer', min_length=2, default='Khun')
    nb: int = Field(description='Combien de fois', gt=0, default=1)