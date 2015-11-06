#coding: utf-8
__author__ = 'lufee'
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FLASKY_ADMIN = 'lufeewu@gmail.com'  # 注册管理员的用户
    FLASKY_POSTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')



config = {
    'default' : ProductionConfig,
}