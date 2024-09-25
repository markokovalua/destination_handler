from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi import FastAPI
from app.db.db import User, db, client
from app.api.routers import all_routers
import json

from app.logger.info_logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )
    destination = "destinations"
    count = await db[destination].count_documents({})
    if count == 0:
        with open("app/config/initial_desitanations.json", "r") as file:
            try:
                await db[destination].create_index([("destinationName", 1)], unique=True)
                await db[destination].insert_many(
                    json.load(file)
                )
            except Exception as exc:
                logger.error(exc)
    yield
    client.close()


app = FastAPI(lifespan=lifespan, description="router-app to handle multiple destinations via specific transports according to routing strategy")


for router in all_routers:
    app.include_router(**router)


# "routingIntents": [
# 		{ "destinationName": "destination1"},
# 		{ "destinationName": "destination2"},
# 		{ "destinationName": "destination3"},
# 		{ "destinationName": "destination4"},
# 		{ "destinationName": "destination5"}
# 	]