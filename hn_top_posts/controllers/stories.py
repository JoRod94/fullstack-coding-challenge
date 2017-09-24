from flask import render_template, Blueprint, url_for
from utils.time_tools import unixToReadable
from hn_top_posts.models import stories
from hn_top_posts.app import app
from hn_top_posts.models import translations

stories_page = Blueprint('stories_page', __name__, template_folder='../templates')

def translate(translation_id):
    translation = translations.get(translation_id)
    if translation is None or translation['status'] != "completed":
        return "Unavailable, try again later"
    else:
        return translation['translatedText']

@stories_page.route('/')
def show():
    top_stories = sorted(stories.get_all(), key=lambda k: k['score'], reverse=True)
    return render_template('stories.html', stories=top_stories, unixToReadable=unixToReadable, get_comments_url=get_comments_url, lang_a=app.config['UNBABEL_TRANSLATION_LANG_A'], lang_b=app.config['UNBABEL_TRANSLATION_LANG_B'], translate=translate)

def get_comments_url(story_id):
    return url_for('comments_page.show')+'?story_id='+str(story_id)

