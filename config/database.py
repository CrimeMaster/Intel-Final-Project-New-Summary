from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:test1234!@cluster0.szfvkcc.mongodb.net/?appName=Cluster0")

db = client.NewsList

collection_name = db["news"]