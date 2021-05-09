from datetime import datetime
from typing import Any, List

from sqlalchemy import Date, cast

from desafio.domain.interactors._entities import (
    Transaction as TransactionEntity,
)
from desafio.domain.repositories._models import ModelRepository, Session, LocalSession
from desafio.domain.repositories._models.accounts import Account as AccountModel
from desafio.domain.repositories._models.transactions import (
    Transaction as TransactionModel,
)


class TransactionRepository(ModelRepository):
    model = TransactionModel
    entity = TransactionEntity

    @classmethod
    def create(cls, entity: Any, session: Session = None) -> Any:
        with LocalSession(session) as session:
            transaction_dict = entity.dict()
            account_dict = transaction_dict.pop("account", {})

            account_model = (
                session.query(AccountModel).filter_by(id=account_dict["id"]).one()
            )
            account_model.balance = account_dict["balance"]

            transaction_model = cls.model(**transaction_dict)
            transaction_model.account = account_model

            session.add(transaction_model)
            session.commit()

        return cls.entity.from_orm(transaction_model)

    @classmethod
    def get_today_withdrawals(
        cls,
        account_id: int,
        session: Session,
    ) -> List[Any]:
        with LocalSession(session) as session:
            query = session.query(cls.model)

            processed_at_date = cast(cls.model.processed_at, Date)
            query = query.filter(processed_at_date == datetime.utcnow().date())

            query = query.filter(cls.model.value < 0)
            query = query.filter_by(account_id=account_id)

            models = query.all()

            entities = [cls.entity.from_orm(model) for model in models]
            return entities
