from datetime import datetime

from pydantic import BaseModel, condecimal


class _Transaction(BaseModel):
    value: condecimal(max_digits=10, decimal_places=2) = None  # type: ignore


class ExposableTransaction(_Transaction):
    id: int
    processed_at: datetime


class CreatableTransaction(_Transaction):
    pass
