from pymongo import MongoClient
from hn_top_posts.app import app

def get_db():
    db_client = MongoClient(app.config['DB_URI'])
    return db_client[app.config['DB_NAME']]

def get_test_db():
    db_client = MongoClient(app.config['DB_URI'])
    return db_client['TEST_DB']