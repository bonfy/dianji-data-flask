# coding:utf-8


from project import db
from datetime import datetime


__author__ = 'bonfy'


class Type(db.Model):

    __tablename__ = 'Type'

    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(50))
    type_en = db.Column(db.String(50))

    created = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, type):
        self.type = type
