import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#basedir = os.path.abspath(os.path.dirname(__file__))
# from sqlalchemy.sql import text)
#app = flaskr(__name__)
#from config import Config
#from flaskr import create_app
#from config import DB_URL
#Config = Config()
#config = current_app.config()
#create_app = create_app()
#from dotenv import load_dotenv
#load_dotenv(os.path.join(basedir, '.env'))
#def get_env_variable(name):
#    try:
#        return os.environ.get(name)
#    except KeyError:
#        message = "Expected environment variable '{}' not set.".format(name)
#        raise Exception(message)
#from dotenv import load_dotenv
#basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(basedir, '.env'))

#flask.cli.load_dotenv(os.path.join(basedir, '.env'))
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_URL = os.environ.get('POSTGRES_URL')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

#DB_URL = 'postgresql+psycopg2//{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PASSWORD,url=POSTGRES_URL,db=POSTGRES_DB)
#DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PASSWORD,url=POSTGRES_URL,db=POSTGRES_DB)
DB_URL = 'postgresql://POSTGRES_USER:POSTGRES_PASSWORD@POSTGRES_URL/POSTGRES_DB'

#engine = create_engine('DB_URL')
engine = create_engine(os.environ.get('DATABASE_URL'))
#engine = create_engine('postgres://postgres:postgres@localhost:5432/postgres')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

#metadata = MetaData(engine).reflect()

#db = SQLAlchemy()
#Session = sessionmaker(engine)
#engine = create_engine(SQLALCHEMY_DATABASE_URI) #db_session =
#scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))
#Base = declarative_base()
#Base.query = db_session.query_property()

#db = SQLAlchemy()
#connection = engine.connect()
#connection = engine.connect()
#raw_cursor = connection()
#def get_session():
#    if 'db_session' not in g:
#        g.session = db_session
#    return g.session

def get_db():
    if 'db' not in g:
        g.db = engine.connect()
        #g.db = connection()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    engine.execute('DROP TABLE IF EXISTS post')
    engine.execute('DROP TABLE IF EXISTS user_tb')
    import flaskr.models
    Base.metadata.create_all(bind=engine)
    #db = get_db()
    #db = engine.connect()
    #file = open('blog/schema.sql')
    #query = file.read().decode('utf8')
    #query = text(file.read())
    #db.execute(file.read().decode('utf8'))
    #db.execute(open('blog/schema.sql').read())
    #with current_app.open_resource('schema.sql') as f:
        #query = text(f.read())
        #db.execute(text(f.read().decode('utf8')))
        #db.execute(text((f.read())

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
