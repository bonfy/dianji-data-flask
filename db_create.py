# coding:utf-8

__author__ = 'BONFY'

from project import db
from project.models import *

# create the database and the db table
db.drop_all()
db.create_all()

# insert data
db.session.add(Type(u'耳机'))
db.session.add(Type(u'摄像'))

db.session.add(Website('http://www.erji.net/', 1))
db.session.add(Website('http://bbs.imp3.net/', 1))
db.session.add(Website('http://bbs.fengniao.com/', 2))

# commit the changes
db.session.commit()
