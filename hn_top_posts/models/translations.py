from hn_top_posts.app import db

def get(translation_id):
    return db.translations.find_one({'_id':translation_id})

def get_all():
    return db.translations.find()

def insert_one(translation):
    return db.translations.insert_one(translation)

def delete_one(translation_id):
    translation = get(translation_id)
    if translation is None:
        return None
    else:
        return db.translations.delete_one({'_id':translation_id})

def delete_all():
    for translation in get_all():
        delete_one(translation['_id'])