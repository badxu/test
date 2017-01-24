#-*-coding:utf8-*-
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json


def towrite(contentdict):
    f.writelines(u'发布时间:' + str(contentdict['topic_release_time']) + '\n')
    f.writelines(u'招标信息:' + contentdict['topic_release_content'] + '\n')


def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[@id="newslist"]/ul/li')
    item = {}
    for each in content_field:
        release_content = each.xpath('span[@class="name"]/a/text()')[0].replace('\r\n','').replace('\t','')
        release_time = each.xpath('span[@class="date"]/text()')[0]
        # print (release_content)
        # print (release_time)
        item['topic_release_content'] = release_content
        item['topic_release_time'] = release_time
        towrite(item)

if __name__ == '__main__':
    pool = ThreadPool(4)
    f = open('mg.txt','a',encoding='utf-8')
    page = []
    for i in range(1,21):
        newpage = 'http://www.mgzbzx.com/article/zbxx/list/' + str(i)
        page.append(newpage)

    results = pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()