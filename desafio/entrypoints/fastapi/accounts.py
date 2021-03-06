from fastapi import HTTPException

from desafio.domain.use_cases.schemas.accounts import (
    CreatableAccount,
    UpdatableAccount,
)
from desafio.domain.use_cases import accounts as account_use_cases
from desafio.domain.exceptions.accounts import AccountNotFound, PersonNotFound
from desafio.entrypoints.fastapi.main import app


@app.post("/accounts", status_code=201)  # type: ignore
async def create_account(account: CreatableAccount):
    try:
        created_account = account_use_cases.create(account)

    except PersonNotFound as error:
        raise HTTPException(status_code=422, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))

    return created_account


@app.get("/accounts/{account_id}")  # type: ignore
async def detail_account(account_id: int):
    try:
        detailed_account = account_use_cases.detail(account_id=account_id)

    except AccountNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))

    return detailed_account


@app.patch("/accounts/{account_id}")  # type: ignore
async def update_account(account_id: int, updatable_account: UpdatableAccount):
    try:
        detailed_account = account_use_cases.update(
            account_id=account_id,
            updatable_account=updatable_account,
        )

    except AccountNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))

    return detailed_account
