from flask import render_template, Blueprint, url_for
from hn_top_posts.db_access import get_db
from utils.time_tools import unixToReadable

stories_page = Blueprint('stories_page', __name__, template_folder='../templates')

@stories_page.route('/')
def show():
    stories = get_top_stories()
    return render_template('stories.html', stories=stories, unixToReadable=unixToReadable, get_comments_url=get_comments_url)

def get_top_stories():
    db = get_db() 
    return sorted(db.stories.find(), key=lambda k: k['score'], reverse=True)

def get_comments_url(story_id):
    return url_for('comments_page.show')+'?post_id='+str(story_id)
