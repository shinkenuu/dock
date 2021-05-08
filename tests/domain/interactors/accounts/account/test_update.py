from desafio.domain.interactors.accounts import AccountInteractor


def test_return(mocker, account):
    # ARRANGE
    account.id = 123

    updating_account = account.copy()
    updating_account.is_active = not bool(account.is_active)
    expected_return = updating_account.dict()

    AccountInteractor.repository = mocker.Mock()
    AccountInteractor.repository.get_one.return_value = account

    AccountInteractor.repository.update.return_value = updating_account

    # ACT
    actual_return = AccountInteractor.update(
        id=account.id,
        is_active=updating_account.is_active,
    )

    # ASSERT
    assert actual_return == expected_return


def test_calls_repository_update_with_updated_entity(mocker, account):
    # ARRANGE
    account.id = 123
    is_active = not bool(account.is_active)

    expected_updating_account = account.copy()
    expected_updating_account.is_active = is_active

    AccountInteractor.repository = mocker.Mock()
    AccountInteractor.repository.get_one.return_value = account

    AccountInteractor.repository.update.return_value = expected_updating_account

    # ACT
    AccountInteractor.update(
        id=account.id,
        is_active=is_active,
    )

    # ASSERT
    AccountInteractor.repository.update.assert_called_once_with(
        expected_updating_account
    )
