# coding: utf-8

from project import db
from datetime import datetime

__all__ = ('User')

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True,
                         nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True, index=True)
    password = db.Column(db.String(100), nullable=False)
    live_days = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        self.token = self.create_token(16)

        if 'password' in kwargs:
            raw = kwargs.pop('password')
            self.password = self.create_password(raw)

        if 'username' in kwargs:
            username = kwargs.pop('username')
            self.username = username.lower()

        if 'email' in kwargs:
            email = kwargs.pop('email')
            self.email = email.lower()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.username

    def __repr__(self):
        return '<Account: %s>' % self.username
