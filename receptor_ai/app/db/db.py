import motor.motor_asyncio
from beanie import Document
from fastapi_users.db import BeanieBaseUser
from fastapi_users_db_beanie import BeanieUserDatabase
import os
from dotenv import load_dotenv
load_dotenv()
# DATABASE_URL = "mongodb://localhost:27017"
DATABASE_URL = os.environ['MONGO_DB_URL']
# DATABASE_URL = "mongodb://root:example@mongodb:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["receptor"]

class User(BeanieBaseUser, Document):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)
