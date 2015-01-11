# coding: utf-8

from project import db
from datetime import datetime

__author__ = 'bonfy'
__all__ = ('Product')

class Product(db.Model):

    __tablename__ = 'Product'

    id = db.Column(db.Integer,primary_key=True)

    # 分类
    # type_id = db.Column(db.Integer, nullable=False)
    # 品牌
    # brand_id = db.Column(db.Integer, nullable=False)
    # 型号
    model_id = db.Column(db.Integer, nullable=False)

    # 买入日期（上架必填）
    buy_dt = db.Column(db.DateTime, nullable=False)
    # 购买价格（上架必填）
    buy_price = db.Column(db.Integer, nullable=False)

    # 成色
    old = db.Column(db.Integer)
    # 照片
    pic = db.Column(db.String(50))
    # 保修期（可填）
    warranty = db.Column(db.DateTime)
    # 心理价位？
    sale_price = db.Column(db.Integer)
    # 备注
    bem = db.Column(db.String(300))
    # 数量
    num = db.Column(db.Integer)
    # 卖 或者 要  1: 卖 0: 要
    buy_sale = db.Column(db.Integer, default=1)
    # 创建日期
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # 创建人
    username = db.Column(db.String(40))

    def __str__(self):
        return self.model_id

    def __repr__(self):
        return '<Product: %s>' % self.model_id