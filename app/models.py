from datetime import datetime
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True,
                      nullable=False)
    username = db.Column(db.String(80), unique=True,
                         nullable=False)
    password = db.Column(db.TEXT, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publication_datetime = db.Column(db.DateTime, nullable=False,
                                     default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),
                        nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publication_datetime = db.Column(db.DateTime, nullable=False,
                                     default=datetime.utcnow)

    def __repr__(self):
        return '<Category %r>' % self.title


