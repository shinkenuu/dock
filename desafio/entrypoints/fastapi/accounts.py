from fastapi import HTTPException

from desafio.domain.controllers.schemas.accounts import (
    CreatableAccount,
)
from desafio.domain.controllers import accounts as account_controllers
from desafio.entrypoints.fastapi.main import app
from desafio.logger import get_logger

LOGGER = get_logger()


@app.post("/accounts", status_code=201)  # type: ignore
async def create_account(account: CreatableAccount):
    try:
        created_account = account_controllers.create_account(account)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))

    return created_account
