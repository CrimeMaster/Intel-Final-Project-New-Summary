from fastapi import FastAPI
from routes.routes import router

from pymongo.mongo_client import MongoClient

app = FastAPI()

app.include_router(router)

