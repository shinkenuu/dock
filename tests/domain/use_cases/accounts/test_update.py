import pytest

from desafio.domain.use_cases.accounts import (
    update,
    AccountInteractor,
    UpdatableAccount,
    ExposableAccount,
)


@pytest.fixture
def mocked_account_interactor_update(mocker):
    return mocker.patch.object(AccountInteractor, "update")


@pytest.fixture
def updatable_account(account):
    return UpdatableAccount(is_active=not bool(account.is_active))


def test_calls_account_interactor_with_updatable_kwargs(
    mocked_account_interactor_update,
    account,
    updatable_account,
):
    # ARRANGE
    mocked_account_interactor_update.return_value = account.dict()
    expected_updatable_dict = {"is_active": updatable_account.is_active}

    # ACT
    update(account_id=account.id, updatable_account=updatable_account)

    # ASSERT
    mocked_account_interactor_update.assert_called_once_with(
        id=account.id,
        **expected_updatable_dict,
    )


def test_returns_exposable_account_equivalent_to_interactor_return(
    mocked_account_interactor_update,
    account,
    updatable_account,
):
    # ARRANGE
    account_kwargs = account.dict()
    mocked_account_interactor_update.return_value = account_kwargs

    expected_exposable_account = ExposableAccount(**account_kwargs)

    # ACT
    actual_account = update(account_id=account.id, updatable_account=updatable_account)

    # ASSERT
    assert actual_account == expected_exposable_account
