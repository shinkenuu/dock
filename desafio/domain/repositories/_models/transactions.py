from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
)

from desafio.domain.repositories._models import Base
from desafio.domain.repositories._models._mixins import InternalIdentifierMixin


class Transaction(Base, InternalIdentifierMixin):
    __tablename__ = "transactions"

    value = Column(Numeric(10, 2), nullable=False)
    processed_at = Column(DateTime, nullable=False)

    account_id = Column(
        BigInteger, ForeignKey("accounts.id"), index=True, nullable=False
    )
