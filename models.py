# coding:utf-8
__author__ = 'lufee'
from flask import Flask
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash

# 创建数据库

basedir = os.getcwd()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    '''
    roles 表格,id 、name 、 default 、 permissions 、 users 关系
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User' : ( Permission.FOLLOW |
                       Permission.COMMENT |
                       Permission.WRITE_ARTICLES, True),
            'Moderator':( Permission.FOLLOW |
                          Permission.COMMENT|
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff,False)   # 拥有所有权限
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None: # 如果添加了新的角色,则自动更新 roles 表格
                role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
            db.session.commit()

    def __repr__(self):
        return '<Role % r>' % self.name

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique = True,index = True)
    email = db.Column(db.String(64),unique = True, index = True)
    password_hash = db.Column(db.String(128))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    # 用户资料
    name = db.Column(db.String)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default = datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    avatar_hash = db.Column(db.String(32))

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Role % r>' % self.username

class Post(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        for i in range(count):
            u_id = randint(0,user_count-1)
            u = User.query.offset( u_id ).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1,5)),
                    timestamp = forgery_py.date.date(True),
                    author = u)
            db.session.add(p)
            db.session.commit()


if __name__ == '__main__':
     posts = Post.query.all()
     for post in posts:
         print post.author.username
     # Role.insert_roles()
     # role = Role.query.all()
     # print role
     # user = User.query.filter_by(username='lufee').first()
     # if user.role is None:
     #     user.role = Role.query.filter_by(permissions=0xff).first()
     #     print user.role
     # db.session.add(user)
     # db.session.commit()
     # user2 = User.query.filter_by(username='lufee').first()
     # print user2.role
     '''
     user = User()
     user.email = 'lufeewu@gmail.com'
     user.username = 'lufee'
     user.password = 'security'
     user.confirmed = True
     db.session.add(user)
     db.session.commit()
     '''
     pass

     #Role.insert_roles()
     #db.create_all()
     #User.generate_fake(10)
     #Post.generate_fake(10)



'''
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)
class User(db.Model):
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
'''
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80),unique= True)
    email = db.Column(db.String(120), unique = True)

    def __init__(self,username,email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r' % self.username
'''