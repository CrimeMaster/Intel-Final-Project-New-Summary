from pydantic import BaseModel

class News(BaseModel):
    Title: str
    wordcount: int
    date: str
    
   