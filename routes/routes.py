from fastapi import APIRouter
from typing import Annotated, Optional
from models.news import News
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

#Get Request Method
@router.get("/")
async def get_news():
    news = list_serial(collection_name.find())
    return news

@router.get("/get-by-Id/{id}")
async def get_By_Id(id: str):
    news_documents = await get_news()
    matching_news = next((item for item in news_documents if item["id"] == id), None)
    return matching_news

@router.get("/get-by-title")
async def get_byTitle(title : Optional[str] = None):
    news_documents = await get_news()
    matching_news = next((item for item in news_documents if item["Title"] == title), None)
    return matching_news

@router.post("/")
async def post_news(news: News):
    collection_name.insert_one(dict(news))
    return news

@router.put("/{id}")
async def put_news(id: str, news: News):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set":dict(news)})

@router.delete("/{id}")
async def delete_news(id:str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})


