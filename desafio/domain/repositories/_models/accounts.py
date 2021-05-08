from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)

from desafio.domain.repositories._models import Base
from desafio.domain.repositories._models._mixins import InternalIdentifierMixin


class Account(Base, InternalIdentifierMixin):
    __tablename__ = "accounts"

    balance = Column(Numeric(10, 2), nullable=False)
    max_daily_withdrawal = Column(Numeric(10, 2))

    is_active = Column(Boolean)
    # type = Column(Integer) # This is not used anywhere, still were at challenge description

    created_at = Column(DateTime, default=datetime.utcnow)

    person_id = Column(BigInteger, ForeignKey("people.id"), nullable=False)


class Person(Base, InternalIdentifierMixin):
    __tablename__ = "people"

    name = Column(String(128))
    cpf = Column(String(11), nullable=False, index=True, unique=True)
    birth_date = Column(Date)
