from fastapi import FastAPI
from app.api.auth import auth
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/auth/openapi.json", docs_url="/api/auth/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(auth, prefix="/api/auth", tags=["auth"])
