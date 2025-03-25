from pydantic import BaseModel, Field


class RegistrationInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
