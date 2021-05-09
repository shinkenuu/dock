from datetime import datetime

from freezegun import freeze_time
import pytest

from desafio.domain.exceptions.accounts import AccountNotFound
from desafio.domain.use_cases.accounts import (
    detail,
    AccountInteractor,
    ExposableAccount,
)


@pytest.fixture
def mocked_account_interactor_find_one(mocker):
    return mocker.patch.object(AccountInteractor, "find_one")


def test_calls_account_interactor_find_one_with_uuid(
    mocked_account_interactor_find_one,
    account,
):
    # ARRANGE
    mocked_account_interactor_find_one.return_value = account.dict()

    # ACT
    detail(account_id=account.id)

    # ASSERT
    mocked_account_interactor_find_one.assert_called_once_with(id=account.id)


def test_raises_account_not_found_from_interactor(
    mocked_account_interactor_find_one,
):
    # ARRANGE
    mocked_account_interactor_find_one.side_effect = AccountNotFound

    # ACT / ASSERT
    with pytest.raises(AccountNotFound):
        detail(account_id=123)


@freeze_time(datetime.utcnow())
def test_returns_exposable_account_equivalent_to_interactor_return(
    mocked_account_interactor_find_one,
    account,
):
    # ARRANGE
    account_kwargs = account.dict()
    mocked_account_interactor_find_one.return_value = account_kwargs

    expected_exposable_account = ExposableAccount(**account_kwargs)

    # ACT
    actual_account = detail(account_id=account.id)

    # ASSERT
    assert actual_account == expected_exposable_account
