def individual_serial(news) -> dict:
    return {
        "id": str(news["_id"]),
        "Title": news["Title"],
        "wordcount": news["wordcount"],
        "date": news["date"]
    }

def list_serial(news) -> list:
    return[individual_serial(n) for n in news]

'''class News(BaseModel):
    Title: str
    wordcount: int
    date: str'''