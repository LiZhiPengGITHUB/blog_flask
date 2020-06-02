from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    telephone =  db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(60), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    hobby = db.Column(db.String(100), nullable=True)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('articles'))  # 反向关系
    '''
    建立User表与Article表的联系，bckref中的参数可以随意填写，但必须前后一致
    若想通过Article表查询User表中的信息，只需要写Article对象.author.User表的属性名
    若想通过User表查询Article表中的信息，只需要写User对象.articles
    '''


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article = db.relationship('Article', backref=db.backref('comments'))
    author = db.relationship('User', backref=db.backref('comments'))


class Film(db.Model):
    __tablename__ = 'film'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500))
    classify = db.Column(db.String(500))
    actors = db.Column(db.Text)
    content = db.Column(db.Text)  # 简介
    cover_url = db.Column(db.String(500))  # 宣传海报
    thunder_url = db.Column(db.String(500))  # 迅雷链接
    magnet_url = db.Column(db.String(500))  # 磁力链接