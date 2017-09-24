from flask import render_template, Blueprint, url_for
from utils.time_tools import unixToReadable
from hn_top_posts.models import stories

stories_page = Blueprint('stories_page', __name__, template_folder='../templates')

@stories_page.route('/')
def show():
    top_stories = stories.get_top_stories()
    return render_template('stories.html', stories=top_stories, unixToReadable=unixToReadable, get_comments_url=get_comments_url)

def get_comments_url(story_id):
    return url_for('comments_page.show')+'?story_id='+str(story_id)
