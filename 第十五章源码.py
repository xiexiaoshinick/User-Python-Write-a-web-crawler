#第15章编写自动爬取网页的爬虫
#15.1 实战items编写
#（1）
D:\Python35\myweb\part15>scrapy startproject autopjt
New Scrapy project 'autopjt', using template directory 'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\Python35\myweb\part15\autopjt
You can start your first spider with:
    cd autopjt
    scrapy genspider example example.com

#(2)
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutopjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#定义好name用来存储商品名
    name=scrapy.Field()
#定义好price用来存储商品价格
    price=scrapy.Field()
#定义好link用来存储商品链接
    link=scrapy.Field()
#定义好comnum用来存储商品评论数
    comnum=scrapy.Field()


#15.2 实战pipelines编写
#(1)
# -*- coding: utf-8 -*-
import codecs
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutopjtPipeline(object):
    def __init__(self):
#打开mydata.json文件
        self.file = codecs.open("D:/python35/myweb/part15/mydata.json", "wb", encoding="utf-8")
    def process_item(self, item, spider):
        i=json.dumps(dict(item), ensure_ascii=False)
#每条数据后加上换行
        line = i + '\n'
#写入数据到mydata.json文件中
        self.file.write(line)
        return item
    def close_spider(self,spider):
#关闭mydata.json文件
        self.file.close()

#(2)
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'autopjt.pipelines.AutopjtPipeline': 300,
}

#(3)
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

#15.4 自动爬虫编写实战
#(1)
D:\Python35\myweb\part15>cd .\autopjt\
D:\Python35\myweb\part15\autopjt>scrapy genspider -t basic autospd dangdang.com
Created spider 'autospd' using template 'basic' in module:
  Autopjt.spiders.autospd

#(2)
# -*- coding: utf-8 -*-
import scrapy
from autopjt.items import AutopjtItem
from scrapy.http import Request

class AutospdSpider(scrapy.Spider):
    name = "autospd"
    allowed_domains = ["dangdang.com"]
    start_urls = (
        'http://category.dangdang.com/pg1-cid4002203.html',
    )

    def parse(self, response):
        item=AutopjtItem()
#通过各Xpath表达式分别提取商品的名称、价格、链接、评论数等信息
        item["name"]=response.xpath("//a[@class='pic']/@title").extract()
        item["price"]=response.xpath("//span[@class='price_n']/text()").extract()
        item["link"]=response.xpath("//a[@class='pic']/@href").extract()
        item["comnum"]=response.xpath("//a[@name='P_pl']/text()").extract()
#提取完后返回item
        yield item
#接下来很关键，通过循环自动爬取75页的数据
        for i in range(1,76):
#通过上面总结的网址格式构造要爬取的网址
            url="http://category.dangdang.com/pg"+str(i)+"-cid4002203.html"
#通过yield返回Request，并指定要爬取的网址和回调函数
#实现自动爬取
            yield Request(url, callback=self.parse)

#15.5 调试与运行
#（1）
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#（2）
# -*- coding: utf-8 -*-
import codecs
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutopjtPipeline(object):
    def __init__(self):
#此时存储到的文件是mydata2.json，不与之前存储的文件mydata.json冲突
        self.file = codecs.open("D:/python35/myweb/part15/mydata2.json", "wb", encoding="utf-8")
    def process_item(self, item, spider):
        #item=dict(item)
        #print(len(item["name"]))
#每一页中包含多个商品信息，所以可以通过循环，每一次处理一个商品
#其中len(item["name"])为当前页中商品的总数，依次遍历
        for j in range(0,len(item["name"])):
#将当前页的第j个商品的名称赋值给变量name
            name=item["name"][j]
            price=item["price"][j]
            comnum=item["comnum"][j]
            link=item["link"][j]
#将当前页下第j个商品的name、price、comnum、link等信息处理一下
#重新组合成一个字典
            goods={"name":name,"price":price,"comnum":comnum,"link":link}
            #将组合后的当前页中第j个商品的数据写入json文件
i=json.dumps(dict(goods), ensure_ascii=False)
            line = i + '\n'
            self.file.write(line)
#返回item
        return item
    def close_spider(self,spider):
        self.file.close()



