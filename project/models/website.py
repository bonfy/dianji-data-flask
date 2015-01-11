# coding:utf-8

from project import db
from datetime import datetime

__author__ = 'bonfy'
__all__ = ('Website')


class Website(db.Model):

    __tablename__ = 'Website'

    id = db.Column(db.Integer, primary_key=True)

    website = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer,nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, website, type_id):
        self.website = website
        self.type_id = type_id