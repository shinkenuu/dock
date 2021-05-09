from datetime import datetime
from decimal import Decimal

from freezegun import freeze_time
import pytest

from desafio.domain.exceptions.accounts import AccountNotFound
from desafio.domain.interactors.transactions import (
    TransactionInteractor,
    Account,
    Transaction,
)


@pytest.fixture()
def account():
    return Account(
        id=2,
        balance=Decimal("1.99"),
        is_active=True,
        created_at=datetime(2020, 1, 1, 0, 0, 0),
        person_id=1,
    )


@pytest.fixture()
def transaction(account):
    value = Decimal("0.01")
    account.balance += value

    return Transaction(
        value=value,
        account_id=account.id,
        processed_at=datetime(2020, 1, 1, 12, 30, 59),
        account=account,
    )


@pytest.fixture()
def mocked_locked_session(mocker):
    locked_session_mock = mocker.MagicMock(name="locked session")

    return mocker.patch(
        "desafio.domain.repositories.decorators.LocalSession",
        new=locked_session_mock,
    )


@pytest.fixture()
def mocked_repository(mocker):
    TransactionInteractor.repository = mocker.Mock()
    return TransactionInteractor.repository


@pytest.fixture()
def mocked_account_interactor(mocker):
    TransactionInteractor.account_interactor = mocker.Mock()
    return TransactionInteractor.account_interactor


def test_return(
    mocked_locked_session,
    mocked_repository,
    mocked_account_interactor,
    account,
    transaction,
):
    # ARRANGE
    mocked_repository.create.return_value = transaction
    mocked_account_interactor.find_one.return_value = account.dict()

    expected_return = {
        "id": None,
        "value": Decimal("0.01"),
        "processed_at": datetime(2020, 1, 1, 12, 30, 59),
        "account_id": 2,
        "account": {
            "balance": Decimal("2.00"),
            "created_at": datetime(2020, 1, 1, 0, 0),
            "id": 2,
            "is_active": True,
            "max_daily_withdrawal": None,
            "person_id": 1,
        },
    }

    # ACT
    with freeze_time("2020-01-01 12:30:59"):
        actual_return = TransactionInteractor.deposit(
            account_id=account.id,
            value=transaction.value,
        )

    # ASSERT
    assert actual_return == expected_return


def test_raises_value_error_when_value_less_than_zero(
    mocked_locked_session,
):
    # ACT / ASSERT
    with pytest.raises(ValueError):
        TransactionInteractor.deposit(
            account_id=2,
            value=Decimal("-3.21"),
        )


def test_raises_account_not_found(
    mocked_locked_session,
    mocked_account_interactor,
):
    # ARRANGE
    mocked_account_interactor.find_one.side_effect = AccountNotFound

    # ACT / Assert
    with pytest.raises(AccountNotFound):
        TransactionInteractor.deposit(
            account_id=2,
            value=Decimal("5.20"),
        )


def test_adds_transaction_value_to_account_balance(
    mocked_locked_session,
    mocked_repository,
    mocked_account_interactor,
    account,
    transaction,
):
    # ARRANGE
    mocked_repository.create.return_value = transaction
    mocked_account_interactor.find_one.return_value = account.dict()

    expected_transaction = transaction.copy()
    expected_transaction.account.balance += transaction.value

    # ACT
    with freeze_time("2020-01-01 12:30:59"):
        TransactionInteractor.deposit(
            account_id=account.id,
            value=transaction.value,
        )

    # ASSERT
    mocked_repository.create.call_args_list[0][0][0] == expected_transaction
