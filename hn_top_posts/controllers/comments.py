from flask import render_template, Blueprint, request
from utils.time_tools import unixToReadable
import threading
from hn_top_posts.models import stories
from hn_top_posts.models import comments
from hn_top_posts.app import db

comments_page = Blueprint('comments_page', __name__, template_folder='../templates')

@comments_page.route('/comments')
def show(): 
    story_id = request.args.get('story_id', type=int)
    story = stories.get(story_id)
    if story is None:
        return "Story not found"
    top_comments = comments.get_top_comments(story)
    return render_template('comments.html', comments=top_comments, story=story, unixToReadable=unixToReadable)