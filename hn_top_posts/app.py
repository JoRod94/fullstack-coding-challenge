from flask import Flask, Blueprint

hn_top_posts = Flask(__name__)
hn_top_posts.config.from_envvar('HN_TOP_POSTS_SETTINGS')

from hn_top_posts.post_updater import update_top_posts
update_top_posts()

from hn_top_posts.controllers.stories import stories_page
hn_top_posts.register_blueprint(stories_page)