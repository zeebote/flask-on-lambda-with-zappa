import os
basedir = os.path.abspath(os.path.dirname(__file__))
def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

POSTGRES_USER = get_env_variable('POSTGRES_USER')
POSTGRES_PASSWORD = get_env_variable('POSTGRES_PASSWORD')
POSTGRES_URL = get_env_variable('POSTGRES_URL')
POSTGRES_DB = get_env_variable('POSTGRES_DB')

DB_URL = 'postgresql+psycopg2//{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PASSWORD,url=POSTGRES_URL,db=POSTGRES_DB)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = DB_URL
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2//{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PASSWORD,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
