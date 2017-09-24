from flask import render_template, Blueprint
from utils.time_tools import unixToReadable
from hn_top_posts.models import translations

translations_page = Blueprint('translations_page', __name__, template_folder='../templates')

@translations_page.route('/translations')
def show():
    requested_translations = translations.get_translations()
    return render_template('stories.html', translations=requested_translations, unixToReadable=unixToReadable)
