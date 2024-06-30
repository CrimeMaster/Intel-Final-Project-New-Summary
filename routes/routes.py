from fastapi import APIRouter
from typing import Annotated, Optional
from models.news import News
from config.database import collection_name
from components.newsData import allNews
from components.news_summary import summarizer
from datetime import datetime
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()
today = datetime.now()

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
async def get_By_Title(title : Optional[str] = None):
    news_documents = await get_news()
    matching_news = next((item for item in news_documents if item["Title"] == title), None)
    if matching_news:
        return matching_news
    else:
        return {"message": "News Title Does Not Exist"}
    
@router.get("/get-by-url")
async def get_By_Url(url: str):
    title , data = allNews(url)

    return {
            "Title": title,
            "wordcount": len(data.split(' ')),
            "date": today.strftime("%B %d, %Y")
        }

@router.get("/get-summary")
async def get_Summary(url: str, summary_len: int):
    title , data = allNews(url)
    summary, doc, scores_df, len_doc, len_summary = summarizer(data, summary_len)

    return {    "OriginalWordCount" : len_doc,
                "SummaryWordCount" : len_summary,
                "Summary" : summary,
                "Scores" : scores_df
            }



    

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


