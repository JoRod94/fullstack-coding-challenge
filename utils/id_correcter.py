#conform to mongodb standards
def id_correcter(item):
    if 'uid' in item:
        item['_id'] = item['uid']
        del item['uid']
    else:
        try:
            item['_id'] = item['id']
            del item['id']
        except KeyError as e:
            print(item)
    return item