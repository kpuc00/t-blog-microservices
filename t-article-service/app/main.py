from fastapi import FastAPI
from app.api.articles import articles
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/articles/openapi.json",
              docs_url="/articles/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(articles, prefix="/articles", tags=["articles"])
