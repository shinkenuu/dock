from typing import List

from desafio.domain.use_cases.schemas.transactions import (
    CreatableTransaction,
    ExposableTransaction,
)
from desafio.domain.interactors.transactions import TransactionInteractor


def list_transactions(account_id: int) -> List[ExposableTransaction]:
    found_transactions = TransactionInteractor.find_many(account_id=account_id)
    return [ExposableTransaction(**transaction) for transaction in found_transactions]


def create_transaction(
    account_id: int, creatable_transaction: CreatableTransaction
) -> ExposableTransaction:
    if creatable_transaction.value == 0:
        raise ValueError("Transaction value must not be 0")

    elif creatable_transaction.value > 0:
        transaction = TransactionInteractor.deposit(
            account_id=account_id,
            value=creatable_transaction.value,
        )

    else:
        transaction = TransactionInteractor.withdrawal(
            account_id=account_id,
            value=creatable_transaction.value,
        )

    return ExposableTransaction(**transaction)
