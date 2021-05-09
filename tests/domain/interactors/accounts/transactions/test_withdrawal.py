from datetime import datetime
from decimal import Decimal

from freezegun import freeze_time
import pytest

from desafio.domain.exceptions.accounts import AccountNotFound
from desafio.domain.exceptions.transactions import (
    InactiveAccount,
    InsufficientFund,
    DailyWithdrawalLimitReached,
)
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
    value = Decimal("-0.99")
    account.balance += value
    assert account.balance >= 0

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
        "value": Decimal("-0.99"),
        "processed_at": datetime(2020, 1, 1, 12, 30, 59),
        "account_id": 2,
        "account": {
            "balance": Decimal("1.00"),
            "created_at": datetime(2020, 1, 1, 0, 0),
            "id": 2,
            "is_active": True,
            "max_daily_withdrawal": None,
            "person_id": 1,
        },
    }

    # ACT
    with freeze_time("2020-01-01 12:30:59"):
        actual_return = TransactionInteractor.withdrawal(
            account_id=account.id,
            value=transaction.value,
        )

    # ASSERT
    assert actual_return == expected_return


def test_raises_value_error_when_value_greater_than_zero(
    mocked_locked_session,
):
    # ACT / ASSERT
    with pytest.raises(ValueError):
        TransactionInteractor.withdrawal(
            account_id=2,
            value=Decimal("3.21"),
        )


def test_raises_account_not_found_from_interactor(
    mocked_locked_session,
    mocked_account_interactor,
):
    # ARRANGE
    mocked_account_interactor.find_one.side_effect = AccountNotFound

    # ACT / Assert
    with pytest.raises(AccountNotFound):
        TransactionInteractor.withdrawal(
            account_id=2,
            value=Decimal("-5.20"),
        )


def test_raises_inactive_account(
    mocked_locked_session, mocked_account_interactor, account
):
    # ARRANGE
    account.is_active = False
    mocked_account_interactor.find_one.return_value = account.dict()

    # ACT / Assert
    with pytest.raises(InactiveAccount):
        TransactionInteractor.withdrawal(
            account_id=2,
            value=Decimal("-5.20"),
        )


def test_raises_insufficient_funds_when_balance_is_less_than_transaction_value(
    mocked_locked_session,
    mocked_account_interactor,
    mocked_repository,
    account,
    transaction,
):
    # ARRANGE
    transaction.value = Decimal("-2.00")
    account.balance = Decimal("1.00")

    mocked_repository.create.return_value = transaction
    mocked_account_interactor.find_one.return_value = account.dict()

    # ACT / Assert
    with pytest.raises(InsufficientFund):
        TransactionInteractor.withdrawal(
            account_id=account.id,
            value=transaction.value,
        )


def test_raises_withdrawal_daily_limit_when_account_today_withdrawals_exceeds_limit(
    mocked_locked_session,
    mocked_account_interactor,
    mocked_repository,
    account,
    transaction,
):
    # ARRANGE
    mocked_repository.get_today_withdrawals.return_value = [
        Transaction(
            id=1,
            value=Decimal("-50.00"),
            account_id=account.id,
            processed_at=transaction.processed_at,
        ),
        Transaction(
            id=2,
            value=Decimal("-50.00"),
            account_id=account.id,
            processed_at=transaction.processed_at,
        ),
    ]

    transaction.value = Decimal("-1.00")
    account.max_daily_withdrawal = Decimal("100.50")

    mocked_repository.create.return_value = transaction
    mocked_account_interactor.find_one.return_value = account.dict()

    # ACT / Assert
    with pytest.raises(DailyWithdrawalLimitReached):
        TransactionInteractor.withdrawal(
            account_id=account.id,
            value=transaction.value,
        )


def test_subtracts_transaction_value_from_account_balance(
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
        TransactionInteractor.withdrawal(
            account_id=account.id,
            value=transaction.value,
        )

    # ASSERT
    mocked_repository.create.call_args_list[0][1] == expected_transaction
