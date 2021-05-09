from fastapi import HTTPException

from desafio.domain.controllers.schemas.transactions import CreatableTransaction
from desafio.domain.controllers import transactions as transaction_controllers
from desafio.domain.exceptions.accounts import AccountNotFound
from desafio.domain.exceptions.transactions import (
    DailyWithdrawalLimitReached,
    InactiveAccount,
    InsufficientFund,
)
from desafio.entrypoints.fastapi.main import app


@app.post("/accounts/{account_id}/transactions", status_code=201)  # type: ignore
async def create_transaction(
    account_id: int, creatable_transaction: CreatableTransaction
):
    try:
        created_transaction = transaction_controllers.create_transaction(
            account_id=account_id,
            creatable_transaction=creatable_transaction,
        )

    except AccountNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))

    except (
        ValueError,
        InactiveAccount,
        InsufficientFund,
        DailyWithdrawalLimitReached,
    ) as error:
        raise HTTPException(status_code=422, detail=str(error))

    return created_transaction


@app.get("/accounts/{account_id}/transactions")  # type: ignore
async def list_transactions(account_id: int):
    try:
        listed_transactions = transaction_controllers.list_transactions(
            account_id=account_id
        )

    except AccountNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))

    return listed_transactions
