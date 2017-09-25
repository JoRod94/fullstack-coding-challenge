import unittest, time, sys
import hn_top_posts
from hn_top_posts.app import app
from hn_top_posts.models import stories
from hn_top_posts.models import comments
from hn_top_posts.models import translations
from hn_top_posts.post_updater import insert_top_story, request_hn_item
from pymongo import MongoClient

def exists_comment_tree(comment_id):
    result = True
    saved_comment = comments.get(comment_id)
    result = result and saved_comment
    if 'kids' in saved_comment:
        for kid_id in saved_comment['kids']:
            result = result and exists_comment_tree(kid_id)
            if not result:
                break
    return result

def exists_translation(translation_id):
    result = True
    saved_translation = translations.get(translation_id)
    return result and saved_translation

class DBTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # test story insertion, its comments, and translations with a sample post https://news.ycombinator.com/item?id=397537
    def test_stories_db(self):
        print("Testing story database insertion...")

        result = True
        test_id = 397537
        sample_story = request_hn_item(test_id)
        insert_top_story(test_id)

        saved_story = stories.get(test_id)
        # It is guaranteed that the story has comments
        result = result and saved_story and 'kids' in saved_story
        for kid_id in saved_story['kids']:
            result = result and exists_comment_tree(kid_id)
            if not result:
                break
        result = result and exists_translation(saved_story['translation_a']) and exists_translation(saved_story['translation_b'])

        assert result

if __name__ == '__main__':
    unittest.main()
