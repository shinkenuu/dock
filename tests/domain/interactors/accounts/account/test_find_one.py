import pytest

from desafio.domain.interactors.accounts import AccountInteractor, AccountNotFound


def test_returns_found_account_from_repository_get_one(mocker, account):
    # ARRANGE
    AccountInteractor.repository = mocker.Mock()
    AccountInteractor.repository.get_one.return_value = account

    expected_account = account.dict()

    # ACT
    actual_account = AccountInteractor.find_one(id=account.id)

    # ASSERT
    assert actual_account == expected_account


def test_calls_repository_get_one_with_kwargs(mocker, account):
    # ARRANGE
    AccountInteractor.repository = mocker.Mock()
    AccountInteractor.repository.get_one.return_value = account

    # ACT
    AccountInteractor.find_one(id=account.id)

    # ASSERT
    AccountInteractor.repository.get_one.assert_called_once_with(id=account.id)


def test_raises_account_not_found_when_repository_returns_none(mocker):
    # ARRANGE
    AccountInteractor.repository = mocker.Mock()
    AccountInteractor.repository.get_one.return_value = None

    # ACT / ASSERT
    with pytest.raises(AccountNotFound):
        AccountInteractor.find_one(
            id=3213,
        )
