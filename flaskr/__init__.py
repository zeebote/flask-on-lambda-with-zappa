import os
from flask import Flask
#from config import Config
#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_object("config.Config")
    app.config.from_object('config.Config')
    #db = SQLAlchemy(app)

    from . import db
    db.init_app(app)
    #with app.app_context():
    #    init_app(app)
    
    #from blog.db import db_session
    #@app.teardown_appcontext
    #def shutdown_session(exception=None):
    #    db_session.remove()
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    #db.init_app(app)

    #with app.app_context():
    #    from . import routes
    #    db.create_all()

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    return app
