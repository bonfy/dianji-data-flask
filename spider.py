# coding:utf-8

__author__ = 'bonfy'


import requests
from bs4 import BeautifulSoup
from project import db
from project.models.scrap import Scrap

website = 'http://www.erji.net/'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'
,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
,'Accept-Encoding':'gzip,deflate,sdch'
,'Accept-Language':'zh-CN,zh;q=0.8'
}


def isDetailUrl(detailUrl):
    if db.session.query(Scrap).filter(Scrap.detailUrl == detailUrl).first():
        print "detailUrl already exits"
        return False
    else:
        print "no such detailUrl"
        return True

for page in range(1, 2):
    default_date = '2015-01-01'
    url = 'http://www.erji.net/thread.php?fid=8&search=&page=%d' % page
    print 'trace url:', url
    r = requests.get(url, headers=headers)

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
        scrap.website_id = 1

        print scrap.detailUrl
        print scrap.postDate
        if scrap.postDate > default_date:
            print 'date is right'
            if isDetailUrl(scrap.detailUrl):
                print 'trace'
                rContent = requests.get(scrap.detailUrl, headers=headers)
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

    db.session.commit()

print 'done'