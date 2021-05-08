from desafio.domain.controllers.schemas.accounts import (
    CreatableAccount,
    ExposableAccount,
)
from desafio.domain.interactors.accounts import AccountInteractor


def create_account(creatable_account: CreatableAccount):
    creatable_account_dict = creatable_account.dict()
    created_account = AccountInteractor.create(**creatable_account_dict)
    return ExposableAccount(**created_account)
