import asyncio
from asyncio.log import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.users import users
from app.api.db import metadata, database, engine
from app.api.rabbitmq.rpc_server import start_listening

metadata.create_all(engine)

app = FastAPI(openapi_url="/users/openapi.json",
              docs_url="/users/docs")

origins = [
    "https://tblog.kstrahilov.dev/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("startup")
async def connect_rabbitmq():
    asyncio.create_task(start_listening())
    logger.info("RPC server started")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(users, prefix="/users", tags=["users"])
