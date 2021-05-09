from datetime import datetime
from decimal import Decimal

from freezegun import freeze_time
import pytest

from desafio.domain.controllers.transactions import (
    create_transaction,
    TransactionInteractor,
    CreatableTransaction,
    ExposableTransaction,
)


@pytest.fixture()
def creatable_transaction(transaction):
    return CreatableTransaction(
        value=transaction.value,
    )


@pytest.fixture()
def exposable_transaction(transaction):
    return ExposableTransaction(
        id=transaction.id,
        value=transaction.value,
        processed_at=transaction.processed_at,
    )


@pytest.fixture
def mocked_transaction_interactor_deposit(mocker):
    return mocker.patch.object(TransactionInteractor, "deposit")


@pytest.fixture
def mocked_transaction_interactor_withdrawal(mocker):
    return mocker.patch.object(TransactionInteractor, "withdrawal")


def test_raises_value_error_when_transaction_value_is_zero(
    account,
    creatable_transaction,
):
    # ARRANGE
    creatable_transaction.value = Decimal("0")

    # ACT / ASSERT
    with pytest.raises(ValueError):
        create_transaction(
            account_id=account.id, creatable_transaction=creatable_transaction
        )


def test_calls_transaction_interactor_deposit_when_value_is_positive(
    mocked_transaction_interactor_deposit,
    account,
    transaction,
    creatable_transaction,
    exposable_transaction,
):
    # ARRANGE
    creatable_transaction.value = Decimal("10.00")
    mocked_transaction_interactor_deposit.return_value = transaction.dict()

    # ACT
    create_transaction(
        account_id=account.id,
        creatable_transaction=creatable_transaction,
    )

    # ASSERT
    mocked_transaction_interactor_deposit.assert_called_once_with(
        account_id=account.id,
        value=creatable_transaction.value,
    )


def test_calls_transaction_interactor_withdrawal_when_value_is_negative(
    mocked_transaction_interactor_withdrawal,
    account,
    transaction,
    creatable_transaction,
    exposable_transaction,
):
    # ARRANGE
    creatable_transaction.value = Decimal("-10.00")
    mocked_transaction_interactor_withdrawal.return_value = transaction.dict()

    # ACT
    create_transaction(
        account_id=account.id,
        creatable_transaction=creatable_transaction,
    )

    # ASSERT
    mocked_transaction_interactor_withdrawal.assert_called_once_with(
        account_id=account.id,
        value=creatable_transaction.value,
    )


@freeze_time(datetime.utcnow())
def test_returns_exposable_transaction_equivalent_to_interactor_return(
    mocked_transaction_interactor_deposit,
    account,
    transaction,
    creatable_transaction,
    exposable_transaction,
):
    # ARRANGE
    creatable_transaction.value = Decimal("10.00")
    mocked_transaction_interactor_deposit.return_value = transaction.dict()

    # ACT
    actual_transaction = create_transaction(
        account_id=account.id,
        creatable_transaction=creatable_transaction,
    )

    # ASSERT
    assert actual_transaction == exposable_transaction
