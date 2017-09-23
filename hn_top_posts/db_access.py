from pymongo import MongoClient
from hn_top_posts.app import hn_top_posts

def get_db():
    db_client = MongoClient(hn_top_posts.config['DB_URI'])
    return db_client[hn_top_posts.config['DB_NAME']]