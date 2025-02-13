from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import requests
import json
from .db_models import Quotes, ENGINE, Base, GoodQuotes
from sqlalchemy.orm import sessionmaker
from .config import GOODREAD_QUOTE_TAG_WITH_URLS
from .unsplash import download_images
from .pexels import download_videos

Base.metadata.create_all(ENGINE)

Session = sessionmaker(bind=ENGINE)
session = Session()
driver = webdriver.Chrome()

class GoodReads():
    def __init__(self):
        self.tag_urls = GOODREAD_QUOTE_TAG_WITH_URLS
    
    def get_rand_page(self, tag):
        lst = list(range(1, 101))
        # get the distinct page numbers from good quotes
        good_p = session.query(GoodQuotes.page).filter(GoodQuotes.tag=="Inspiration").distinct().all()
        # remove the page numbers from the list if the page has been scraped
        if good_p:
            good_p = [p[0] for p in good_p]
            for p in good_p:
                lst.remove(p)
        return random.choice(lst)
        

    def get_quote_from_tags(self):
        tag = random.choice(list(self.tag_urls.keys()))
        page_num = self.get_rand_page(tag)
        driver.get(self.tag_urls[tag] + f"?page={page_num}")
        quotes = driver.find_elements(By.CLASS_NAME, "quoteText")
        count = 0
        for quote in quotes:
            quote_text = quote.text.replace(chr(8220), '').replace(chr(8221), '').replace("\n", " ").split("―")[0]
            if len(quote_text) > 200 or len(quote_text) < 30:
                print(f"Skipping: quote is either too long or too short")
                continue
            new_quote = GoodQuotes(quote=quote_text, tag=tag, vid_shown=False, widget_shown=False, page=page_num)
            session.add(new_quote)
            count += 1
        print(f"{count} quotes for {tag} added from page {page_num}")
        session.commit()
        # download_images(tag)
        download_videos(tag)

class zenQuotes():
    def __init__(self):
        self.url = "https://zenquotes.io/api/quotes/"
    
    def get_quote(self):
        resp = requests.get(self.url)
        quotes = [quote["q"] for quote in resp.json()]
        
        for quote in quotes:
            new_quote = Quotes(quote=quote, vid_shown=False, widget_shown=False)
            session.add(new_quote)
        session.commit()
        
if __name__ == "__main__":
    good = GoodReads()
    good.get_quote_from_tags()