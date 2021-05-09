import pytest

from desafio.domain.use_cases.accounts import (
    create,
    AccountInteractor,
    CreatableAccount,
    ExposableAccount,
)


@pytest.fixture
def mocked_account_interactor_create(mocker):
    return mocker.patch.object(AccountInteractor, "create")


@pytest.fixture
def creatable_account(account):
    return CreatableAccount(**account.dict())


def test_calls_account_interactor_with_creatable_account_kwargs(
    mocked_account_interactor_create,
    account,
    creatable_account,
):
    # ARRANGE
    mocked_account_interactor_create.return_value = account.dict()
    expected_creatable_dict = creatable_account.dict()

    # ACT
    create(creatable_account)

    # ASSERT
    mocked_account_interactor_create.assert_called_once_with(**expected_creatable_dict)


def test_returns_exposable_account_equivalent_to_interactor_return(
    mocked_account_interactor_create,
    account,
    creatable_account,
):
    # ARRANGE
    account_kwargs = account.dict()
    mocked_account_interactor_create.return_value = account_kwargs

    expected_exposable_account = ExposableAccount(**account_kwargs)

    # ACT
    actual_account = create(creatable_account)

    # ASSERT
    assert actual_account == expected_exposable_account
