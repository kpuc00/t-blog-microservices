from fastapi import FastAPI
from app.api.comments import comments
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/comments/openapi.json",
              docs_url="/api/comments/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(comments, prefix="/api/comments", tags=["comments"])
