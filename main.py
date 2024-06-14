from fastapi import FastAPI

from db.config import create_db_and_tables
from routers import users_router

create_db_and_tables()
app = FastAPI()
app.include_router(users_router)


@app.get("/")
async def index():
    return {"message": "Hello World"}


if __name__ == '__main__': # pragma: no cover
    from uvicorn import run
    run(app, host="0.0.0.0", port=8000)