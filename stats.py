from const import *
import feedparser
from tinydb import TinyDB, Query
import requests
import json

if __name__ == "__main__":  
    db = TinyDB(DB_PATH)
    Article = Query()
    total = len(db)
    imported = db.count(Article.status == STATUS_IMPORTED)
    published = db.count(Article.status == STATUS_PUBLISHED)
    print(f"Total: {total} Waiting: {imported} Published: {published}")