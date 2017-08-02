#第14章Scrapy中文输出与存储
#14.1 Scrapy的中文输出
#(1)
# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class MypjtItem(scrapy.Item):
    # define the fields for your item here like:
    # 定义title，用来存储网页标题信息
    title=scrapy.Field()
    
#(2)
# -*- coding: utf-8 -*-
import scrapy
#导入items文件中的MypjtItem
from mypjt.items import MypjtItem
class MyspdSpider(scrapy.Spider):
    name = "myspd"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
#定义要抓取的起始网址为新浪首页
        'http://www.sina.com.cn/',
    )
    def parse(self, response):
#初始化item
        item=MypjtItem()
#通过Xpath表达式提取该网页中的标题信息
        item["title"]=response.xpath("/html/head/title").extract()
#输出提取到的标题信息
        print item["title"]

#(3)
# -*- coding: utf-8 -*-
import scrapy
from mypjt.items import MypjtItem
class MyspdSpider(scrapy.Spider):
    name = "myspd"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
        'http://www.sina.com.cn/',
    )
    def parse(self, response):
        item=MypjtItem()
        item["title"]=response.xpath("/html/head/title").extract()
        #print item["title"]
# item["title"]是一个列表，所以我们可以通过for循环遍历出该列表中的元素
        for i in item["title"]:
#对遍历出来的标题信息进行encode("gbk")编码
            print i.encode("gbk")

#(4)
D:\Python35\myweb\part13>scrapy startproject mypjt
New Scrapy project 'mypjt', using template directory 'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\Python35\myweb\part13\mypjt

You can start your first spider with:
    cd mypjt
    scrapy genspider example example.com

#(5)
# -*- coding: utf-8 -*-
import scrapy
class MypjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()

#(6)
# -*- coding: utf-8 -*-
import scrapy
from mypjt.items import MypjtItem
class WeisuenSpider(scrapy.Spider):
    name = "weisuen"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
#设置起始网址为新浪新闻下的某个新闻网页
        'http://tech.sina.com.cn/d/s/2016-09-17/doc-ifxvyqwa3324638.shtml',
    )

    def parse(self, response):
        item=MypjtItem()
#通过Xpath表达式提取网页中的标题信息
        item["title"]=response.xpath("/html/head/title/text()")
#直接输出，在Python3.X中，虽然包含中文信息，但直接输出即可
        print(item["title"])

#14.2 Scrapy的中文存储
#(1)
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#本项目中在pipelines文件里面的类是MypjtPipeline，接下来会具体看到
    'mypjt.pipelines.MypjtPipeline': 300,
}

#(2)
# -*- coding: utf-8 -*-
#导入codecs模块，使用codecs直接进行解码
import codecs
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#定义了pipelines里面的类，类名需要与刚才settings.py里面设置的类名对应起来
class MypjtPipeline(object):
#__init__()为类的初始化方法，开始的时候调用
    def __init__(self):
#首先以写入的方式创建或打开一个普通文件用于存储抓取到的数据
        self.file = codecs.open("D:/python35/myweb/part13/mydata1.txt", "wb", encoding="utf-8")
#process_item()为pipelines中的主要处理方法，默认会自动调用
    def process_item(self, item, spider):
#设置每行要写的内容
        l = str(item) + '\n'
#此处通过print()输出，方便程序的调试
        print(l)
#将对应信息写入文件中
        self.file.write(l)
        return item
#close_spider()方法一般在关闭蜘蛛时调用
    def close_spider(self,spider):
#关闭文件，有始有终
        self.file.close()

#14.3 输出中文到json文件
#(1)
# -*- coding: utf-8 -*-
import codecs
#因为要进行JSON文件的处理，所以导入json模块
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
class MypjtPipeline(object):
    def __init__(self):
#以写入的方式创建或打开一个json格式（后缀名为.json）的文件
        self.file = codecs.open("D:/python35/myweb/part13/mydata1.json", "wb", encoding="utf-8")
    def process_item(self, item, spider):
#通过dict(item)将item转化成一个字典
#然后通过json模块下的dumps()处理字典数据
        i=json.dumps(dict(item))
#得到的数据后加上”\n”换行符形成要写入的一行数据
        line = i + '\n'
#在此进行直接输出，方便调试，实际的时候输出这一行可以去掉
        print(line)
#写入数据到json文件中
        self.file.write(line)
        return item
    def close_spider(self,spider):
#关闭文件，有始有终
        self.file.close()

#(2)
# -*- coding: utf-8 -*-
import codecs
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MypjtPipeline(object):
    def __init__(self):
        self.file = codecs.open("D:/python35/myweb/part13/mydata1.json", "wb", encoding="utf-8")
    def process_item(self, item, spider):
#通过json模块下的dumps()处理的时候
#第二个参数将ensure_ascii设置为False
        i=json.dumps(dict(item), ensure_ascii=False)
        line = i + '\n'
        print(line)
        self.file.write(line)
        return item
    def close_spider(self,spider):
        self.file.close()

#(3)
   start_urls = (
        'http://tech.sina.com.cn/d/s/2016-09-17/doc-ifxvyqwa3324638.shtml',
        "http://sina.com.cn",
    )

#(4)
  item["title"]=response.xpath("/html/head/title/text()").extract()
        item["key"]=response.xpath("//meta[@name='keywords']/@content").extract()



