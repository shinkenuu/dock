from decimal import Decimal

from pydantic import BaseModel


class _Transaction(BaseModel):
    value: Decimal


class ExposableTransaction(_Transaction):
    id: int


class CreatableTransaction(_Transaction):
    pass
