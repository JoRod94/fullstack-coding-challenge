from flask import Flask, Blueprint
from pymongo import MongoClient

hn_top_posts = Flask(__name__)
hn_top_posts.config.from_envvar('HN_TOP_POSTS_SETTINGS')

from hn_top_posts.controllers.stories import stories_page
hn_top_posts.register_blueprint(stories_page)

def get_db():
    db_client = MongoClient('DB_URI')
    return db_client[hn_top_posts.config['DB_NAME']]