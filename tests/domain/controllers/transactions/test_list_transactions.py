from datetime import datetime

from freezegun import freeze_time
import pytest

from desafio.domain.controllers.transactions import (
    list_transactions,
    TransactionInteractor,
    ExposableTransaction,
)


@pytest.fixture
def mocked_transaction_interactor_find_many(mocker):
    return mocker.patch.object(TransactionInteractor, "find_many")


def test_calls_transaction_interactor_find_many_with_account_id(
    mocked_transaction_interactor_find_many,
    account,
    transaction,
):
    # ARRANGE
    mocked_transaction_interactor_find_many.return_value = [transaction.dict()]

    # ACT
    list_transactions(account_id=account.id)

    # ASSERT
    mocked_transaction_interactor_find_many.assert_called_once_with(
        account_id=account.id
    )


@freeze_time(datetime.utcnow())
def test_returns_exposable_transaction_equivalent_to_interactor_return(
    mocked_transaction_interactor_find_many,
    account,
    transaction,
):
    # ARRANGE
    transaction_kwargs = transaction.dict()
    mocked_transaction_interactor_find_many.return_value = [transaction_kwargs]

    expected_exposable_transactions = [ExposableTransaction(**transaction_kwargs)]

    # ACT
    actual_transactions = list_transactions(account_id=account.id)

    # ASSERT
    assert actual_transactions == expected_exposable_transactions
