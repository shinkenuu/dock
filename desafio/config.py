from os import getenv

DATABASE_URL = getenv(
    "DATABASE_URL", "postgresql://username:password@127.0.0.1/desafio"
)
PORT = int(getenv("PORT", "8080"))
