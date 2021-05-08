from desafio.domain.controllers.schemas.accounts import (
    CreatableAccount,
    ExposableAccount,
    UpdatableAccount,
)
from desafio.domain.interactors.accounts import AccountInteractor


def detail(account_id: int):
    found_account = AccountInteractor.find_one(id=account_id)
    return ExposableAccount(**found_account)


def create(creatable_account: CreatableAccount):
    creatable_account_dict = creatable_account.dict()
    created_account = AccountInteractor.create(**creatable_account_dict)
    return ExposableAccount(**created_account)


def update(account_id: int, updatable_account: UpdatableAccount):
    updatable_account_dict = updatable_account.dict(exclude_unset=True)
    updated_account = AccountInteractor.update(id=account_id, **updatable_account_dict)
    return ExposableAccount(**updated_account)
