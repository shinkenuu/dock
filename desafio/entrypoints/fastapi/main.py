import uvicorn  # type: ignore
from fastapi import FastAPI

from desafio.config import PORT

app = FastAPI()

from desafio.entrypoints.fastapi.health_check import *  # noqa
from desafio.entrypoints.fastapi.accounts import *  # noqa
from desafio.entrypoints.fastapi.transactions import *  # noqa

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
