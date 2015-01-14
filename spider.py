# coding:utf-8

__author__ = 'bonfy'


from spider import *
import schedule
import time
import datetime

def job():
    print datetime.datetime.utcnow()
    # wait to add Threading
    sp1 = Spider(1, page=2)
    sp2 = Spider(2, page=2)
    sp3 = Spider(3, page=2)
    sp1.run()
    sp2.run()
    sp3.run()

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)