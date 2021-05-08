from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime


class CreationTimeTrackerMixin:
    created_at = Column(DateTime, default=datetime.utcnow)


class InternalIdentifierMixin:
    id = Column(BigInteger, primary_key=True)
