import requests
from hn_top_posts.models import translations
from hn_top_posts.app import app

request_headers={"Authorization": "ApiKey "+app.config['UNBABEL_SANDBOX_USERNAME']+":"+app.config['UNBABEL_SANDBOX_KEY'], 
                "Content-Type": "application/json"}

base_translation_url="https://sandbox.unbabel.com/tapi/v2/translation/"

def request_translation(text, lang_to):
    data = {}
    data["text"] = text
    data["target_language"] = lang_to
    data["text_format"] = "text"
    text_data = str(data).replace('\'', '\"')
    response = requests.post(base_translation_url, headers=request_headers, data=text_data)
    translation = correct_id_form(response.json())
    translations.insert_one(translation)
    return response.json()

def check_translation(translation_id):
    response = requests.get(base_translation_url+str(translation_id)+"/",headers=request_headers)
    new_translation = correct_id_form(response.json())
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

#conform to mongodb standards
def correct_id_form(translation):
    translation['_id'] = translation['uid']
    del translation['uid']
    return translation