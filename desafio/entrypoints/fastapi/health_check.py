from desafio.entrypoints.fastapi.main import app


@app.get("/healthcheck")  # type: ignore
async def health_check():
    return {"status": "OK"}
