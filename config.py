import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FIRST_TIME_SETUP = False
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASSWORD = 'R3public'
    DEFAULT_ADMIN_EMAIL = 'admin@example.com'
    ADMIN_GROUP_NAME = 'administrators'
    BOOTSTRAP_SERVE_LOCAL = True
    #Update later - need consistent manor for storing environment variable (I know this should be easy)
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'
    POSTS_PER_PAGE = 3