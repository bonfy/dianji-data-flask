# coding:utf-8

from project import db
from datetime import datetime

__author__ = 'bonfy'
__all__  = ('Model')

class Model(db.Model):
    __tablename__ = 'Model'

    id = db.Column(db.Integer, primary_key=True)

    brand_id = db.Column(db.Integer,nullable=False)
    model = db.Column(db.String(50),nullable=False)
    model_en = db.Column(db.String(50))

    created = db.Column(db.DateTime, default=datetime.utcnow)