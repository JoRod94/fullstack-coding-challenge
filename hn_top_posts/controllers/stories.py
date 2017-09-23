from flask import render_template, Blueprint
from hn_top_posts.db_access import get_db
from utils.time_tools import unixToReadable

stories_page = Blueprint('stories_page', __name__, template_folder='../templates')

@stories_page.route('/')
def show():
    stories = get_top_stories()
    return render_template('stories.html', stories=stories, unixToReadable=unixToReadable)

def get_top_stories():
    db = get_db() 
    return sorted(db.stories.find(), key=lambda k: k['score'], reverse=True)
