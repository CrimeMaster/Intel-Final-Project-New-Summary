##Import Modules
from bs4 import BeautifulSoup 

#Remove this after testing
import requests
import pandas as pd

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'} 

url = "https://indianexpress.com/article/india/confident-of-win-bjp-plans-political-event-to-celebrate-likely-over-weekend-9368360/"

def allNews(url):
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find("h1").get_text()
    all_paragraphs = soup.find_all('p')
    news = ""
    for paragraph in all_paragraphs:
        para = paragraph.get_text()
        para = para.strip()
        news += para
    return title, news

