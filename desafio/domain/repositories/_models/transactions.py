from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship, backref

from desafio.domain.repositories._models import Base
from desafio.domain.repositories._models._mixins import InternalIdentifierMixin


class Transaction(Base, InternalIdentifierMixin):
    __tablename__ = "transactions"

    value = Column(Numeric(10, 2), nullable=False)
    processed_at = Column(
        DateTime, default=datetime.utcnow
    )  # TODO Maybe index for daily withdrawal calculation

    account_id = Column(
        BigInteger, ForeignKey("accounts.id"), index=True, nullable=False
    )
    account = relationship("Account", backref=backref("transactions", lazy="dynamic"))
