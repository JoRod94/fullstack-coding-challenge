import sched, time, json, threading, requests
from hn_top_posts.app import app,db
from hn_top_posts.models import stories
from hn_top_posts.models import comments

top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
item_url = 'https://hacker-news.firebaseio.com/v0/item/'

def start_updater():
    s = sched.scheduler(time.time, time.sleep)
    updater_thread = threading.Thread(target=update_top_posts, kwargs={'s':s})
    updater_thread.start()

def update_top_posts(s):
    top_ids = json.loads(requests.get(top_stories_url).content)
    del top_ids[app.config['NR_POSTS']:]
    threads = []
    for story_id in top_ids:
        thread = threading.Thread(target=insert_top_story, kwargs={'story_id': story_id})
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()

    all_stories = stories.get_all()
    for story in all_stories:
        story_id = story['_id']
        if story_id not in top_ids:
            stories.delete_one(story_id)

    s.enter(app.config['POST_REFRESH_PERIOD'], 1, update_top_posts, kwargs={'s':s})
    s.run()

def insert_top_story(story_id):
    stories.delete_one(story_id)
    story = json.loads(requests.get(item_url+str(story_id)+".json").content)
    #change id name to comply with mongoDB standards
    story['_id'] = story['id']
    del story['id']

    #comments are inserted first to prevent showing the story comments page with incomplete comments
    threads = []
    if 'kids' in story:
        for kid_id in story['kids']:
            thread = threading.Thread(target=insert_comment, kwargs={'comment_id': kid_id})
            threads.append(thread)
            thread.start()
    for t in threads:
        t.join()

    write_result = stories.insert_one(story)

    # Remove comments if story write was unsuccessful
    if not write_result.acknowledged:
        if 'kids' in story:
            for kid_id in story['kids']:
                comments.delete_one(kid_id)

def insert_comment(comment_id):
    comment = json.loads(requests.get(item_url+str(comment_id)+".json").content)
    #change id name to comply with mongoDB standards
    comment['_id'] = comment['id']
    del comment['id']
    write_result = comments.insert_one(comment)
    threads = []
    if write_result.acknowledged and 'kids' in comment:
        for kid_id in comment['kids']:
            thread = threading.Thread(target=insert_comment, kwargs={'comment_id': kid_id})
            threads.append(thread)
            thread.start()
    for t in threads:
        t.join()