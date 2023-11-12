from pydantic import BaseModel

class CreateTransactionDto(BaseModel):
    name: str
    money: float
    type: str
    use_type: str