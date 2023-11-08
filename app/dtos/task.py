from pydantic import BaseModel

class CreateTransactionDto(BaseModel):
    name: str
    money: float
    type: str