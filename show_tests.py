import unittest, time, sys
import hn_top_posts
from hn_top_posts.app import app
from hn_top_posts.models import stories
from hn_top_posts.models import comments
from hn_top_posts.models import translations
from pymongo import MongoClient

def descendants_of(item):
    result = 0
    if 'kids' in item:
        for kid_id in item['kids']:
            result += 1 + descendants_of(comments.get(kid_id))
    return result

class ShowTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # asserts correct number of stories in stories page after 30 seconds
    def test_stories_show(self):
        print("Testing correct number of stories after 30 seconds...")
        time.sleep(30)
        rv = self.app.get('/')
        nr_stories = str(rv.data).count("class=\"story row\"")
        print("Comparison: ", nr_stories, "", app.config['NR_POSTS'])
        assert nr_stories == app.config['NR_POSTS']

    # asserts correct number of comments for a story after 30 seconds
    def test_story_comments_show(self):
        print("Testing correct number of comments after 30 seconds...")
        db_stories = stories.get_all()
        result = True
        for story in db_stories:
            comments_show = self.app.get('/comments?story_id='+str(story['_id']))
            nr_comments = str(comments_show.data).count("comment-box")
            descendants = descendants_of(story)
            print("Comparison", nr_comments, descendants)
            correct_number = nr_comments == descendants
            result = result and correct_number
            if not result:
                break
        assert result

    # asserts correct number of translations in translations page after 30 seconds
    def test_translations_show(self):
        print("Testing correct number of translations after 30 seconds...")
        rv = self.app.get('/translations')
        nr_translations = str(rv.data).count("<tr>")
        print("Comparison: ", nr_translations, "", app.config['NR_POSTS']*2 + 1)
        assert nr_translations == app.config['NR_POSTS']*2 + 1

if __name__ == '__main__':
    unittest.main()
