# coding:utf-8

from project import db
from datetime import datetime

from _base import SessionMixin

__author__ = 'bonfy'
__all__ = ('Scrap')


class Scrap(db.Model, SessionMixin):
    __tablename__ = 'Scrap'

    id = db.Column(db.Integer, primary_key=True)

    # type: 耳机 或者 摄像
    # type_id = db.Column(db.Integer) 这个关联到 website
    # 关键字 耳机、音响 之类
    keyWord = db.Column(db.String(50))
    # 标题
    title = db.Column(db.String(400))
    # 点title出来的详细页面
    detailUrl = db.Column(db.String(300))
    # 正文
    content = db.Column(db.Text)
    # 发帖时间
    postDate = db.Column(db.DateTime)
    # 回复数
    replyCount = db.Column(db.Integer)
    # 浏览数
    viewCount = db.Column(db.Integer)
    # 最后回复用户
    lastReplyName = db.Column(db.String(100))
    # 最后回复时间
    lastReplyDate = db.Column(db.DateTime)
    # 来自网站 erji.hk / bbs.imp3.net 之类
    website_id = db.Column(db.Integer)
    # 插入数据库时间
    insertDate = db.Column(db.DateTime, default=datetime.utcnow())

    # 商品名称
    pdtName = db.Column(db.String(100))
    # 商品数量
    pdtNum = db.Column(db.String(10))
    # 商品成色
    pdtNew = db.Column(db.String(100))
    # 商品价格
    pdtPrice = db.Column(db.String(50))
    # 所在地
    pdtLocation = db.Column(db.String(100))
    # 交易方式
    pdtSaleWay = db.Column(db.String(100))
    # 运费 卖方承担运费 买方承担等
    pdtTransFee = db.Column(db.String(100))
    # 联系方式
    pdtTel = db.Column(db.String(50))
    # 信息有效期
    pdtValidTime = db.Column(db.String(20))
    # 商品描述
    pdtDes  = db.Column(db.Text)
    # 商品链接
    pdtUrl = db.Column(db.String(500))
    # 求购 出售、其他
    pdtSale = db.Column(db.String(50))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'keyWord': self.keyWord,
            'title': self.title
        }