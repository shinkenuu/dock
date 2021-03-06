from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal


class Person(BaseModel):
    id: Optional[int]
    name: str
    cpf: str
    birth_date: Optional[datetime]

    class Config:
        orm_mode = True


class Account(BaseModel):
    id: Optional[int]
    balance: condecimal(max_digits=10, decimal_places=2)  # type: ignore
    max_daily_withdrawal: condecimal(max_digits=10, decimal_places=2) = None  # type: ignore

    is_active: Optional[bool]
    created_at: datetime

    person_id: int

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    id: Optional[int]
    value: condecimal(max_digits=10, decimal_places=2) = None  # type: ignore
    processed_at: datetime

    account_id: int
    account: Optional[Account]

    class Config:
        orm_mode = True
