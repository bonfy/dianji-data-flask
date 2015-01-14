# coding:utf-8

__author__ = 'bonfy'


__all__ = ('Spider',)

import requests
from project.models import Scrap
from config import SPIDER_DATE, SPIDER_PAGE, SPIDER_HEADER
from project import db
from bs4 import BeautifulSoup
import re


class Spider(object):

    def __init__(self, website_id
                 , default_date=SPIDER_DATE
                 , page=SPIDER_PAGE
                 , headers=SPIDER_HEADER):
        self.website_id = website_id
        self.default_date = default_date
        self.page = page
        self.headers = headers

    def run(self):
        if self.website_id == 1:
            self.spider_erjinet()
        elif self.website_id == 2:
            self.spider_imp3()
        elif self.website_id == 3:
            self.spider_fengniao()

    # 判断此url 是否已经抓取过
    def isDetailUrl(self, detail_url):
        if db.session.query(Scrap).filter(Scrap.detailUrl == detail_url).first():
            print "detailUrl already exits"
            return False
        else:
            print "no such detailUrl"
        return True

    def spider_erjinet(self):
        website = 'http://www.erji.net/'
        for page in xrange(1, self.page):
            url = 'http://www.erji.net/thread.php?fid=8&search=&page=%d' % page
            print 'trace url:', url
            r = requests.get(url, headers=self.headers)
            # print r.encoding
            # r.encoding 实际值 为  'ISO-8859-1'
            # 关键的转码
            r.encoding = 'gbk'
            soup = BeautifulSoup(r.text,"html.parser")
            trMineGroups = soup.findAll('tr',{'class':'tr3 t_one'})

            for trMine in trMineGroups:
                tdMineGroups = trMine.findAll('td')

                scrap = Scrap()

                scrap.title = tdMineGroups[1].find('a').get_text()#.replace(u'\xa0',u' ')
                scrap.detailUrl = website + tdMineGroups[0].find('a').get('href')
                scrap.author = tdMineGroups[2].find('a').get_text()
                scrap.postDate = tdMineGroups[2].find('div').get_text()
                scrap.keyWord = tdMineGroups[1].get_text()[tdMineGroups[1].get_text().find('[')+1:tdMineGroups[1].get_text().find(']')]
                scrap.replyCount = int(tdMineGroups[3].get_text().strip())
                scrap.viewCount = int(tdMineGroups[4].get_text().strip())
                scrap.lastReplyName = tdMineGroups[5].get_text()[tdMineGroups[5].get_text().find('by: ')+len('by: '):]
                scrap.lastReplyDate = tdMineGroups[5].find('a').get_text().strip()
                scrap.website_id = self.website_id

                print scrap.detailUrl
                print scrap.postDate
                if scrap.postDate > self.default_date:
                    print 'date is right'
                    if self.isDetailUrl(scrap.detailUrl):
                        print 'trace'
                        rContent = requests.get(scrap.detailUrl, headers=self.headers)
                        rContent.encoding = 'gbk'
                        rSoup = BeautifulSoup(rContent.text, "html.parser")
                        if rSoup.find('div', {'class': 'tpc_content'}):
                            scrap.content = rSoup.find('div', {'class': 'tpc_content'}).get_text()
                        else:
                            scrap.content = 'TimeOut or some error'
                        try:
                            print scrap
                            db.session.add(scrap)
                        except Exception as e:
                            print e
                            print str(scrap.content)
                            print 'error in title:', scrap.title
                    else:
                        'date is too old'

                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print 'insert Table error,Error is',e

    def spider_fengniao(self):
        website = 'http://bbs.fengniao.com'
        for page in xrange(1, self.page):
            # http://bbs.fengniao.com/forum/forumdisplay.php?f=81&type=list&page=1&sort=threadid&order=desc#new
            url = 'http://bbs.fengniao.com/forum/forumdisplay.php?f=81&type=list&page=%d&sort=threadid&order=desc#new' % page
            # print url
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")

            tbs = soup.findAll('table',{'class':'dkopex'})

            if len(tbs) == 2:
                tb = tbs[1]
            elif len(tbs) == 1:
                tb = tbs[0]
            else:
                print 'something error with table'
                break

            trs = tb.findAll('tr')
            for tr in trs:
                tds = tr.findAll('td')
                scrap = Scrap()

                scrap.title = tds[1].find('a').get_text()
                scrap.detailUrl = website + tds[1].find('a').get('href')
                scrap.author = tds[2].find('a').get_text()
                scrap.postDate = tds[2].find('p', {'class':'time'}).get_text()
                scrap.keyWord = ''
                scrap.replyCount = int(tds[3].get_text().strip())
                scrap.viewCount = int(tds[4].get_text().strip())
                scrap.lastReplyName = tds[6].find('a',{'rel':'nofollow'}).get_text().strip()
                # need to 解析'今天  几月几日之类'
                scrap.lastReplyDate = '1999-01-01'
                scrap.website_id = self.website_id

                print scrap.detailUrl
                print scrap.postDate

                if scrap.postDate > self.default_date:
                    print 'date is right'
                    if self.isDetailUrl(scrap.detailUrl):
                        print 'trace'
                        rContent = requests.get(scrap.detailUrl, headers=self.headers)
                        rSoup = BeautifulSoup(rContent.text, "html.parser")
                        if rSoup.find('div', {'class': 'mainContent'}):
                            scrap.content = rSoup.find('div', {'class': 'mainContent'}).get_text().strip()
                        else:
                            scrap.content = 'TimeOut or some error'
                        try:
                            print scrap
                            db.session.add(scrap)
                        except Exception as e:
                            print e
                            print str(scrap.content)
                            print 'error in title:', scrap.title
                    else:
                        'date is too old'
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print 'insert Table error,Error is',e


    def spider_imp3(self):
        for page in xrange(1, self.page):
            url = 'http://bbs.imp3.net/forum-63-%d.html' % page
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text,"html.parser")
            trGroups = soup.find_all("tbody",id=re.compile("normalthread_"))

            for trMine in trGroups:
                scrap = Scrap()

                try:
                    scrap.title = trMine.find('a',class_="s xst").get_text()
                    scrap.detailUrl = trMine.find('a',class_="s xst").get('href')

                    emList = trMine.find_all('em')
                    scrap.keyWord = emList[0].get_text()[1:-1]
                    scrap.sale = emList[1].get_text()[1:-1]
                    scrap.postDate = emList[2].get_text()
                    scrap.viewCount = int(emList[3].get_text().strip())
                    scrap.lastReplyDate = emList[4].get_text()
                    scrap.replyCount = int(trMine.find('a',class_="xi2").get_text().strip())

                    userList = trMine.find_all('cite')
                    scrap.author = userList[0].find('a').get_text()
                    scrap.lastReplyName = userList[0].find('a').get_text()
                    scrap.website_id = self.website_id
                except Exception as e:
                    print 'error with:', url
                    print e

                print scrap.detailUrl
                print scrap.postDate

                if scrap.postDate > self.default_date:
                    print 'date is right'
                    if self.isDetailUrl(scrap.detailUrl):
                        print 'trace'
                        rContent = requests.get(scrap.detailUrl, headers=self.headers)
                        rSoup = BeautifulSoup(rContent.text, "html.parser")
                        rtable = rSoup.find("table",class_="cgtl mbm")


                        if rtable:
                            scrap.pdtSale = rtable.caption.get_text().strip()

                            print scrap.pdtSale

                            if scrap.pdtSale != u'其它话题':
                                if rtable.findAll("tr"):
                                    trs = rtable.findAll("tr")
                                    scrap.pdtName = trs[0].td.get_text().strip()
                                    scrap.pdtNum = trs[1].td.get_text().strip()
                                    scrap.pdtNew = trs[2].td.get_text().strip()
                                    scrap.pdtPrice = trs[3].td.get_text().strip()
                                    scrap.pdtLocation = trs[4].td.get_text().strip()
                                    scrap.pdtSaleWay = trs[5].td.get_text().strip()
                                    scrap.pdtTransFee = trs[6].td.get_text().strip()
                                    scrap.pdtTel = trs[7].td.get_text().strip()
                                    scrap.pdtValidTime = trs[8].td.get_text().strip()
                                    if scrap.pdtSale == u'求购':
                                        scrap.pdtDes = ''
                                        scrap.pdtUrl = ''
                                    else:
                                        scrap.pdtDes = trs[9].td.get_text().strip()
                                        scrap.pdtUrl = trs[10].td.get_text().strip()
                        if rSoup.find('td',id = re.compile("postmessage")):
                            scrap.content = rSoup.find('td',id = re.compile("postmessage")).get_text().strip()
                        else:
                            scrap.content = 'TimeOut or some error'
                        try:
                            print scrap
                            db.session.add(scrap)
                        except Exception as e:
                            print e
                            print str(scrap.content)
                            print 'error in title:', scrap.title
                    else:
                        'date is too old'
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print 'insert Table error,Error is', e