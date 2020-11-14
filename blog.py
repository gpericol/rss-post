from const import *
import sys
import os
import pickle
from oauth2client import client
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from tinydb import TinyDB, Query

def get_blogger_service_obj():
    creds = None
    if os.path.exists(BLOGGER_AUTH_PICKLE):
        with open(AUTH_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(BLOGGER_AUTH_PICKLE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(AUTH_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    blog_service = build('blogger', 'v3', credentials=creds)

    return blog_service

if __name__ == "__main__":  
    db = TinyDB('db.json')
    Article = Query()
    values = db.search(Article.status == STATUS_IMPORTED)

    if len(values) == 0:
        print("No articles")
        exit()
    
    article = min(values, key=lambda x: x['article_date'])

    if DEBUG:
        print(article)

    video_link = 'https://www.youtube.com/embed/' + article['article_id'].split(':')[-1]
    data = {
        'content': f'<iframe width="560" height="315" src="{video_link}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
        'title': article['article_title'],
        'labels' : [article['feed_title']],
        'blog': {
            'id': BLOG_ID
        },
    }

    blog_handler = get_blogger_service_obj()

    posts = blog_handler.posts()
    res = posts.insert(blogId=BLOG_ID, body=data, isDraft=False, fetchImages=True).execute()

    db.update({'status': STATUS_PUBLISHED}, Article.article_id == article['article_id'])


