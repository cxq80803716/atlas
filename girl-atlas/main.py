#coding:utf-8
import random
import urllib2
import urllib,os
from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Pool
seed_url = 'http://girl-atlas.net/'
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Host':'girl-atlas.net',
           'Referer':'http://girl-atlas.net/',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def get_href(url):
    hrefs = []
    request = urllib2.Request(url,headers=headers)
    html = urllib2.urlopen(request,timeout=10).read()
    html = str(html)
    soup = BeautifulSoup(html)
    datas = soup.findAll('div',{'class':'col-md-11 col-sm-11'})
    titles = []
    for data in datas:
        href = data.find('a').get('href')
        title = data.find('a').string
        titles.append(title)
        hrefs.append(href)
    return hrefs,titles

def get_src(href):
    url = seed_url + href
    request = urllib2.Request(url,headers=headers)
    html = urllib2.urlopen(request,timeout=10).read()
    html = str(html)
    soup = BeautifulSoup(html)
    datas = soup.findAll('li',{'class':'slide '})
    src_hrefs = []
    for data in datas:
        src_href = data.find('img').get('src')
        if src_href == None: src_href = data.find('img').get('delay')
        src_hrefs.append(src_href)
    return src_hrefs

def download_src(src_href,header,filename):
    try:
        request = urllib2.Request(src_href,headers=header)
        resp = urllib2.urlopen(request,timeout=10)
        fp = open(filename,'wb')
        fp.write(resp.read())
        fp.close()
        return True
    except:
        return False
def save_src(src_hrefs,title,href):
    header = { 'Referer':seed_url + href,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    path = u'D:\\atlas\%s\\' % title.decode()
    if not os.path.exists(path):
        os.makedirs(path)
    pool = Pool(10)
    count = 1
    retry = 0
    for src_href in src_hrefs:
        filename = path + u'%d.jpg' % count
        count +=1
        if not pool.apply_async(download_src,(src_href,header,filename)):
            retry +=1
            if retry > 5:
                print u'Download %s fail!' % title.decode()
                return False
    pool.close()
    pool.join()
    print u'Download %s success!' % title.decode()
    
if __name__ == '__main__':
    url = seed_url + '?p='
    page = 1
    while True:
        sleep(random.uniform(2,4))
        url = seed_url + '?p=' + str(page)
        hrefs,titles = get_href(url)
        if len(hrefs) == 0: break
        for i in range(len(hrefs)):
            src_hrefs = get_src(hrefs[i])
            save_src(src_hrefs,titles[i],hrefs[i])
        page +=1
#     
    