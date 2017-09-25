import sched, time, json, threading, requests
from hn_top_posts.app import app,db
from hn_top_posts.models import stories
from hn_top_posts.models import comments
from hn_top_posts.translation_manager import request_translation
from utils.id_correcter import id_correcter

top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
item_url = 'https://hacker-news.firebaseio.com/v0/item/'

def start_updater():
    s = sched.scheduler(time.time, time.sleep)
    updater_thread = threading.Thread(target=update_top_posts, kwargs={'s':s})
    updater_thread.start()

def update_top_posts(s):
    top_ids = json.loads(requests.get(top_stories_url).content)
    del top_ids[app.config['NR_POSTS']:]

    for story in stories.get_all():
        if story['_id'] not in top_ids:
            story.delete_one(story['_id'])

    threads = []
    for story_id in top_ids:
        thread = threading.Thread(target=insert_top_story, kwargs={'story_id': story_id})
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()

    s.enter(app.config['POST_REFRESH_PERIOD'], 1, update_top_posts, kwargs={'s':s})
    s.run()

def insert_top_story(story_id):
    new_story = request_hn_item(story_id)
    new_story = id_correcter(new_story)

    current_story = stories.get(story_id)
    if current_story is None:
        new_story['translation_a'] = request_translation(new_story['title'], app.config['UNBABEL_TRANSLATION_LANG_A'])
        new_story['translation_b'] = request_translation(new_story['title'], app.config['UNBABEL_TRANSLATION_LANG_B'])
    else:
        new_story['translation_a'] = current_story['translation_a']
        new_story['translation_b'] = current_story['translation_b']
        stories.delete_one_keep_translations(story_id)

    #comments are inserted first to prevent showing the story comments page with incomplete comments
    threads = []
    if 'kids' in new_story:
        for kid_id in new_story['kids']:
            thread = threading.Thread(target=insert_comment, kwargs={'comment_id': kid_id})
            threads.append(thread)
            thread.start()
    for t in threads:
        t.join()

    write_result = stories.insert_one(new_story)

    # Remove comments if story write was unsuccessful
    if not write_result.acknowledged:
        if 'kids' in new_story:
            for kid_id in new_story['kids']:
                comments.delete_one(kid_id)

def insert_comment(comment_id):
    comment = request_hn_item(comment_id)
    comment = id_correcter(comment)
    write_result = comments.insert_one(comment)
    threads = []
    if write_result.acknowledged and 'kids' in comment:
        for kid_id in comment['kids']:
            thread = threading.Thread(target=insert_comment, kwargs={'comment_id': kid_id})
            threads.append(thread)
            thread.start()
    for t in threads:
        t.join()

def request_hn_item(item_id):
    return json.loads(requests.get(item_url+str(item_id)+".json").content)