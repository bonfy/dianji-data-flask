# coding:utf-8

__author__ = 'bonfy'

from spider import *
import schedule
import time
import datetime
import threading, thread

class MyThread(threading.Thread):
    """docstring for MyThread"""

    def __init__(self, id,page) :
        super(MyThread, self).__init__()
        self.id = id
        self.page = page

    def run(self):
        print "Starting trace", self.id
        sp = Spider(self.id, page=self.page)
        sp.run()
        print "Exiting trace", self.id


def job():

    print datetime.datetime.utcnow()
    threadList = []

    jobs = [
        {'id': 1, 'page': 2},
        {'id': 2, 'page': 2},
        {'id': 3, 'page': 2}
    ]

    for item in jobs:
        id = item['id']
        page = item['page']
        print 'trace id : ', id
        thread = MyThread(id,page)
        #开启线程
        thread.start()
        threadList.append(thread)

    for thread in threadList:
        thread.join()

    print 'Exit'


'''

def job():

    # wait to add Threading
    sp1 = Spider(1, page=2)
    sp2 = Spider(2, page=2)
    sp3 = Spider(3, page=2)
    sp1.run()
    sp2.run()
    sp3.run()
'''
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)