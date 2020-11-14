from const import *
import feedparser
from tinydb import TinyDB, Query
import facebook
import requests
import json


def get_feed(db, feed_link):
    feed = feedparser.parse(feed_link)
    feed_title = feed.feed.title
    feed_entries = feed.entries

    Article = Query()
    
    for entry in feed.entries:
        article_title = entry.title
        article_id = entry.id
        article_date = entry.published

        value = db.search(Article.article_id == article_id)
        
        if len(value) == 0:
            db.insert({
                'feed': feed_link,
                'feed_title': feed_title,
                'article_id': article_id,
                'article_title': article_title,
                'article_date': article_date, 
                'status': STATUS_IMPORTED
            })

            if DEBUG:
                print (f"{article_title}[{article_id}]")
        else:
            if DEBUG:
                print (f"skipped {article_id}")

if __name__ == "__main__":  
    db = TinyDB(DB_PATH)
    with open(CHANNELS_PATH) as f:
        feed_links = json.load(f)

    for feed_link in feed_links:
        print(f"Getting {feed_link['name']}")
        get_feed(db, feed_link['url'])