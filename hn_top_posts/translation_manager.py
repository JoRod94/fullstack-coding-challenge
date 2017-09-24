import requests, json, sched, time, threading
from hn_top_posts.models import translations
from hn_top_posts.app import app
from utils.id_correcter import id_correcter
from hn_top_posts.models import translations

request_headers={"Authorization": "ApiKey "+app.config['UNBABEL_SANDBOX_USERNAME']+":"+app.config['UNBABEL_SANDBOX_KEY'], 
                "Content-Type": "application/json"}

base_translation_url="https://sandbox.unbabel.com/tapi/v2/translation/"

def start_periodic_translation_checker():
    s = sched.scheduler(time.time, time.sleep)
    threading.Thread(target=periodic_translation_checker, kwargs={'s':s}).start()

def periodic_translation_checker(s):
    for translation in translations.get_all():
        check_translation(translation['_id'])
    s.enter(app.config['TRANSLATION_REFRESH_PERIOD'], 1, periodic_translation_checker, kwargs={'s':s})
    s.run()

def request_translation(text, lang_to):
    data = {}
    data["text"] = text
    data["target_language"] = lang_to
    data["source_language"] = "en"
    data["text_format"] = "text"
    text_data = json.dumps(data)
    response = requests.post(base_translation_url, headers=request_headers, data=text_data.encode('utf-8'))
    translation = id_correcter(response.json())
    translations.insert_one(translation)
    return translation['_id']

def check_translation(translation_id):
    response = requests.get(base_translation_url+str(translation_id)+"/",headers=request_headers)
    new_translation = id_correcter(response.json())
    current_translation = translations.get(translation_id)
    if current_translation is not None:
        current_status = current_translation['status']
        new_status = new_translation['status']
        if current_status != new_status:
            translations.delete_one(new_translation['_id'])
            translations.insert_one(new_translation)
    else:
        translations.insert_one(new_translation)
    return new_translation