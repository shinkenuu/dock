from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Account(BaseModel):
    id: Optional[int]
    balance: Decimal
    max_daily_withdrawal: Optional[Decimal]

    is_active: Optional[bool]
    type: int

    created_at: datetime

    person_id: int

    class Config:
        orm_mode = True


class Person(BaseModel):
    id: Optional[int]
    name: str
    cpf: str
    birth_date: Optional[datetime]

    class Config:
        orm_mode = True
