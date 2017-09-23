from flask import Flask, Blueprint

app = Flask(__name__)
app.config.from_envvar('HN_TOP_POSTS_SETTINGS')

from hn_top_posts.post_updater import start_updater
start_updater()

from hn_top_posts.controllers.stories import stories_page
app.register_blueprint(stories_page)