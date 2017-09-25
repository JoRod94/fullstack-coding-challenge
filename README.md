# Implementation Comments

### Python 3.6.0 Required

To set up this implementation, the following modules are required (recommended pip installation):

- flask
- pymongo
- requests

The app also requires a settings file, whose path is obtained from the `HN_TOP_POSTS_SETTINGS` environment variable, add using `export HN_TOP_POSTS_SETTINGS=/path/to/settings.py`.

This file needs to have the following settings (sample values):

~~~~ 
DB_NAME = 'top_posts_db'
DB_URI = 'mongodb://localhost:27017/'
POST_REFRESH_PERIOD = 600 #seconds
TRANSLATION_REFRESH_PERIOD = 5 #seconds
NR_POSTS = 10
UNBABEL_SANDBOX_USERNAME="<api_username>"
UNBABEL_SANDBOX_KEY="<api_key>"
UNBABEL_TRANSLATION_LANG_A="pt"
UNBABEL_TRANSLATION_LANG_B="de"
~~~~

After starting a `mongod` process, run the app using `python run.py`. 

Access the app at `http://localhost:5000`.

Test using `python view_tests.py` for view tests and `python db_tests.py` for database tests.



# Unbabel Fullstack Challenge

Hey :smile:

Welcome to our Fullstack Challenge repository. This README will guide you on how to participate in this challenge.

In case you are doing this to apply for our open positions for a Fullstack Developer make sure you first check the available jobs at [https://unbabel.com/jobs](https://unbabel.com/jobs)

Please fork this repo before you start working on the challenge. We will evaluate the code on the fork.

**FYI:** Please understand that this challenge is not decisive if you are applying to work at [Unbabel](https://unbabel.com/jobs). There are no right and wrong answers. This is just an opportunity for us both to work together and get to know each other in a more technical way.

## Challenge


#### Build a multilingual Hackernews.

Create a multilingual clone of the Hackernews website, showing just the top 10 most voted news and their comments. 
This website must be kept updated with the original hackernews website (every 10 minutes).

Translations must be done using the Unbabel API in sandbox mode. (Ask whoever has been in contact with you about the credentials)

Build a dashboard to check the status of all translations.


#### Requirements
* Use Flask web framework
* Use Bootstrap
* For MongoDB
* Create a scalable application. 
* Only use Unbabel's Translation API on sandbox mode
* Have the news titles translated to 2 languages
* Have unit tests


#### Notes
* We dont really care much about css but please dont make our eyes suffer. 
* Page load time shouldnt exceed 2 secs 


#### Resources
* Unbabel's API: http://developers.unbabel.com/
* Hackernews API: https://github.com/HackerNews/API

