from flask import render_template, Blueprint

stories_page = Blueprint('stories_page', __name__, template_folder='../templates')
@stories_page.route('/')
def show():
    stories = []
    return render_template('stories.html', stories=stories)
