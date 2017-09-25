from hn_top_posts.app import db
from hn_top_posts.models import comments
from hn_top_posts.models import translations

def get(story_id):
    return db.stories.find_one({'_id':story_id})

def get_all():
    return db.stories.find()

def insert_one(story):
    return db.stories.insert_one(story)

# useful for replace, more efficient translation management
def delete_one_keep_translations(story_id):
    story = get(story_id)
    if story is None:
        return None
    else:
        if 'kids' in story:
            for kid_id in story['kids']:
                comments.delete_one(kid_id)
        return db.stories.delete_one({'_id':story_id})

def delete_one(story_id):
    story = get(story_id)
    if story is None:
        return None
    else:
        if 'kids' in story:
            for kid_id in story['kids']:
                comments.delete_one(kid_id)
        translations.delete_one(story['translation_a'])
        translations.delete_one(story['translation_b'])
        return db.stories.delete_one({'_id':story_id})

def delete_all():
    for story in get_all():
        delete_one(story['_id'])