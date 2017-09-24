from hn_top_posts.app import db

def get_top_comments(story):
    top_comments = []
    if 'kids' in story:
        for comment_id in story['kids']:
            top_comment = get_comment_tree(comment_id)
            if 'deleted' in top_comment and top_comment['deleted'] is True:
                top_comment['text'] = "deleted"
            top_comments.append(top_comment)
    # ordered by time, since comment score is hidden
    return sorted(top_comments, key=lambda k: k['time'])

def get_comment_tree(comment_id):
    comment = get(comment_id)
    sub_comments = []
    if 'kids' in comment:
        for kid_id in comment['kids']:
            sub_comment = get_comment_tree(kid_id)
            if 'deleted' in sub_comment and sub_comment['deleted'] is True:
                sub_comment['text'] = "deleted"
            sub_comments.append(sub_comment)
    # ordered by time, since comment score is hidden
    comment['sub_comments'] = sorted(sub_comments, key=lambda k: k['time'])
    return comment

def get(comment_id):
    result = db.comments.find_one({'_id':comment_id})
    return db.comments.find_one({'_id':comment_id})

def insert_one(comment):
    return db.comments.insert_one(comment)

def delete_one(comment_id):
    comment = get(comment_id)
    if comment is None:
        return None
    else:
        if 'kids' in comment:
            for kid_id in comment['kids']:
                delete_one(kid_id)
        return db.comments.delete_one({'_id':comment_id})

def delete_all():
    for comment in get_all():
        delete_one(comment['_id'])