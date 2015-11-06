# coding:utf-8
__author__ = 'lufee'
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_moment import Moment
from flask_pagedown import PageDown

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name]) # 加载app的config
    # config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .upload import upload as upload_blueprint
    app.register_blueprint(upload_blueprint, url_prefix='/upload')

    return app