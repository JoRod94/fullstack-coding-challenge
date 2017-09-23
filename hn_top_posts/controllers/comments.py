from flask import render_template, Blueprint, request
from hn_top_posts.db_access import get_db
from utils.time_tools import unixToReadable
import threading

comments_page = Blueprint('comments_page', __name__, template_folder='../templates')

db = get_db()

@comments_page.route('/comments')
def show():
    post_id = request.args.get('post_id', type=int)
    post = db.stories.find_one({'_id':post_id})
    comments = get_top_comments(post)
    return render_template('comments.html', comments=comments, post=post, unixToReadable=unixToReadable)

def get_top_comments(post):
    top_comments = []
    if 'kids' in post:
        for comment_id in post['kids']:
            top_comments.append(get_comment_tree(comment_id))
    # ordered by time, since comment score is hidden
    return sorted(top_comments, key=lambda k: k['time'])

def get_comment_tree(comment_id):
    comment = db.comments.find_one({'_id':comment_id})
    sub_comments = []
    if 'kids' in comment:
        for kid_id in comment['kids']:
            sub_comments.append(get_comment_tree(kid_id))
    # ordered by time, since comment score is hidden
    comment['sub_comments'] = sorted(sub_comments, key=lambda k: k['time'])
    return comment
