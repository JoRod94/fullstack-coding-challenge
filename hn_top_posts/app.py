from flask import Flask, Blueprint
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_envvar('HN_TOP_POSTS_SETTINGS')

db_client = MongoClient(app.config['DB_URI'])
db = db_client[app.config['DB_NAME']]

db.stories.drop()
db.comments.drop()
db.translations.drop()

from hn_top_posts.post_updater import start_updater
start_updater()

from hn_top_posts.translation_manager import start_periodic_translation_checker
start_periodic_translation_checker()

from hn_top_posts.controllers.stories import stories_page
app.register_blueprint(stories_page)

from hn_top_posts.controllers.translations import translations_page
app.register_blueprint(translations_page)

from hn_top_posts.controllers.comments import comments_page
app.register_blueprint(comments_page)