from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, StrictBool


class _Account(BaseModel):
    balance: Decimal
    type: int  # Ain't this supposed to be an Enum?
    person_id: int


class ExposableAccount(_Account):
    id: int
    max_daily_withdrawal: Optional[Decimal]
    is_active: Optional[StrictBool]


class CreatableAccount(_Account):
    max_daily_withdrawal: Optional[Decimal]
    is_active: Optional[StrictBool]


class Person(BaseModel):
    name: str
    cpf: str
    birth_date: Optional[datetime]
