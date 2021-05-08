from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal, StrictBool


class _Account(BaseModel):
    balance: condecimal(max_digits=10, decimal_places=2)  # type: ignore
    person_id: int

    max_daily_withdrawal: condecimal(max_digits=10, decimal_places=2) = None  # type: ignore
    is_active: Optional[StrictBool]


class ExposableAccount(_Account):
    id: int
    created_at: datetime


class CreatableAccount(_Account):
    pass


class UpdatableAccount(BaseModel):
    is_active: StrictBool


class Person(BaseModel):
    name: str
    cpf: str
    birth_date: Optional[datetime]
