from fastapi import FastAPI
from app.api.users import user
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/user/openapi.json", docs_url="/api/user/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(user, prefix="/api/user", tags=["user"])
