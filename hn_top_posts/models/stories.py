from hn_top_posts.app import db
from hn_top_posts.models import comments

def get_top_stories():
  return sorted(db.stories.find(), key=lambda k: k['score'], reverse=True)

def get(story_id):
    return db.stories.find_one({'_id':story_id})

def insert_one(story):
    return db.stories.insert_one(story)

def delete_one(story_id):
    story = get(story_id)
    if story is None:
        return None
    else:
        if 'kids' in story:
            for kid_id in story['kids']:
                comments.delete_one(kid_id)
        return db.stories.delete_one({'_id':story_id})