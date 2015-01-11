# coding:utf-8

from project import db
from datetime import datetime

__author__ = 'bonfy'
__all__ = ('Brand')


class Brand(db.Model):

    __tablename__ = 'Brand'

    id = db.Column(db.Integer, primary_key=True)

    type_id = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    brand_en = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)