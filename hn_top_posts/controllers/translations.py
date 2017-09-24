from flask import render_template, Blueprint
from utils.time_tools import unixToReadable
from hn_top_posts.models import translations

translations_page = Blueprint('translations_page', __name__, template_folder='../templates')

@translations_page.route('/translations')
def show():
    requested_translations = sorted(translations.get_all(), key=lambda k: k['target_language'], reverse=True)
    return render_template('translations.html', translations=requested_translations, unixToReadable=unixToReadable)
