import requests
import json
import threading
from hn_top_posts.db_access import get_db

top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
item_url = 'https://hacker-news.firebaseio.com/v0/item/'
db = get_db()

def update_top_posts():
    top_ids = json.loads(requests.get(top_stories_url).content)
    del top_ids[10:]
    for story_id in top_ids:
        threading.Thread(target=insert_top_story, kwargs={'story_id': story_id}).start()

def insert_top_story(story_id):
    story = json.loads(requests.get(item_url+str(story_id)+".json").content)
    #change id name to comply with mongoDB standards
    story['_id'] = story['id']
    del story['id']
    write_result = db.stories.insert_one(story)
    if write_result.acknowledged and 'kids' in story:
        for kid_id in story['kids']:
            threading.Thread(target=insert_comment, kwargs={'comment_id': kid_id}).start()

def insert_comment(comment_id):
    comment = json.loads(requests.get(item_url+str(comment_id)+".json").content)
    #change id name to comply with mongoDB standards
    comment['_id'] = comment['id']
    del comment['id']
    write_result = db.comments.insert_one(comment)
    if write_result.acknowledged and 'kids' in comment:
        for kid_id in comment['kids']:
            threading.Thread(target=insert_comment, kwargs={'comment_id': kid_id}).start()