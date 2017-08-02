#第19章千图网图片爬虫项目
#
#（1）
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QtpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#建立picurl存储图片的网址
    picurl=scrapy.Field()
#建立picid存储图片网址中的图片名，以方便构造本地文件名
    picid=scrapy.Field()

#（2）
# -*- coding: utf-8 -*-
import urllib.request
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QtpjtPipeline(object):
    def process_item(self, item, spider):
#一个图片列表页中有多张图片，通过for循环依次将图片存储到本地
        for i in range(0,len(item["picurl"])):
            thispic=item["picurl"][i]
#根据上面总结的规律构造出原图片的URL地址
            trueurl=thispic+"_1024.jpg"
#构造出图片在本地存储的地址
            localpath = "D:/Python35/myweb/part19/pic/" + item["picid"][i] + ".jpg"
#通过urllib.request.urlretrieve()将原图片下载到本地
            urllib.request.urlretrieve(trueurl, filename=localpath)
        return item

#（3）
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'qtpjt.pipelines.QtpjtPipeline': 300,
}


#（4）
# -*- coding: utf-8 -*-
import scrapy
import re
from qtpjt.items import QtpjtItem
from scrapy.http import Request

class QtspdSpider(scrapy.Spider):
    name = "qtspd"
    allowed_domains = ["58pic.com"]
    start_urls = (
        'http://www.58pic.com/tb/',
    )

    def parse(self, response):
        item=QtpjtItem()
#构建提取缩略图网址的正则表达式
        paturl="(http://pic.qiantucdn.com/58pic/.*?).jpg"
        #提取对应图片网址
item["picurl"]=re.compile(paturl).findall(str(response.body))
#构造出提取图片名的正则表达式，以方便构造出本地的文件名
        patlocal = "http://pic.qiantucdn.com/58pic/.*?/.*?/.*?/(.*?).jpg"
#提取互联网中的图片名
        item["picid"] = re.compile(patlocal).findall(str(response.body))
        yield item
#通过for循环依次遍历1到200页图片列表页
        for i in range(1,201):
#构造出下一页图片列表页的网址
            nexturl="http://www.58pic.com/tb/id-"+str(i)+".html"
            yield Request(nexturl, callback=self.parse)





