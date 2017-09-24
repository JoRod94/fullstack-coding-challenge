import unittest, time, sys
import hn_top_posts
from hn_top_posts.app import app
from hn_top_posts.models import stories
from hn_top_posts.models import comments
from pymongo import MongoClient

def descendants_of(item):
    result = 0
    if 'kids' in item:
        for kid_id in item['kids']:
            result += 1 + descendants_of(comments.get(kid_id))
    return result

class TestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # asserts correct number of stories in stories page after 20 seconds
    def test_stories_show(self):
        print("Testing correct number of stories after 20 seconds...")
        time.sleep(20)
        rv = self.app.get('/')
        nr_stories = str(rv.data).count("class=\"story row\"")
        print("Comparison: ", nr_stories, "", app.config['NR_POSTS'])
        assert nr_stories == app.config['NR_POSTS']

    def test_story_comments_show(self):
        print("Testing correct number of comments after 20 seconds...")
        time.sleep(20)
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

if __name__ == '__main__':
    unittest.main()
