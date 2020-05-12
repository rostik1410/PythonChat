from datetime import datetime

from flask_login import UserMixin

from chat_app import db

chat_users = db.Table('chat_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    nickname = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password = db.Column(db.String(100))
    messages = db.relationship('Message', back_populates='author')


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_name = db.Column(db.String(64))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    chat_users = db.relationship('User', secondary=chat_users, lazy='subquery',
                                 backref=db.backref('chats', lazy=True))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates="messages")
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    text = db.Column(db.String(1000))
