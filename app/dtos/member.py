from pydantic import BaseModel

class CreateMemberDto(BaseModel):
    username: str
    email: str
    password: str