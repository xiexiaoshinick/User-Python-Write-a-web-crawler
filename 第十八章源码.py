#第十八章 第四篇 实战项目案例
#18.3 和讯博客爬虫项目编写实战
#（1）
Create database hexun;

#(2)
Use hexun;
Create table myhexun(id int(10) auto_increment primary key not null,name varchar(30),url varchar(100),hits int(15),comment int(15));

#(3)
D:\Python35\myweb\part18>scrapy startproject hexunpjt
New Scrapy project 'hexunpjt', using template directory 'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\Python35\myweb\part18\hexunpjt
You can start your first spider with:
    cd hexunpjt
    scrapy genspider example example.com

#(4)
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HexunpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#建立name存储文章名
    name= scrapy.Field()
#建立url存储文章url网址
    url= scrapy.Field()
#建立hits存储文章阅读数
    hits= scrapy.Field()
#建立comment存储文章评论数
    comment= scrapy.Field()

#(5)
# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HexunpjtPipeline(object):

    def __init__(self):
        #刚开始时连接对应数据库
        self.conn=pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="hexun")

    def process_item(self, item, spider):
        #每一个博文列表页中包含多篇博文的信息，我们可以通过for循环一次处理各博文的信息
        for j in range(0, len(item["name"])):
            # 将获取到的name、url、hits、comment分别赋给各变量
            name=item["name"][j]
            url=item["url"][j]
            hits=item["hits"][j]
            comment=item["comment"][j]
            #构造对应的sql语句，实现将获取到的对应数据插入数据库中
            sql="insert into myhexun(name,url,hits,comment) VALUES('"+name+"','"+url+"','"+hits+"','"+comment+"')"
            #通过query实现执行对应的sql语句
            self.conn.query(sql)
        return item


    def close_spider(self,spider):
        # 最后关闭数据库连接
        self.conn.close()

#(6)

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'hexunpjt.pipelines.HexunpjtPipeline': 300,
}

#(7)
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

#(8)
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

#(9)
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#(10)
# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from hexunpjt.items import HexunpjtItem
from scrapy.http import Request

class MyhexunspdSpider(scrapy.Spider):
    name = "myhexunspd"
    allowed_domains = ["hexun.com"]
    #设置要爬取的用户的uid，为后续构造爬取网址做准备
    uid = "19940007"
    #通过start_requests方法编写首次的爬取行为
    def start_requests(self):
        #首次爬取模拟成浏览器进行
        yield Request("http://"+str(self.uid)+".blog.hexun.com/p1/default.html",headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})


    def parse(self, response):
        item = HexunpjtItem()
        item['name']=response.xpath("//span[@class='ArticleTitleText']/a/text()").extract()
        item["url"]=response.xpath("//span[@class='ArticleTitleText']/a/@href").extract()
        #接下来需要使用urllib和re模块获取博文的评论数和阅读数
        #首先提取存储评论数和点击数网址的正则表达式
        pat1='<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'
        #hcurl为存储评论数和点击数的网址
        hcurl=re.compile(pat1).findall(str(response.body))[0]
        # 模拟成浏览器
        headers2 = ("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers2]
        # 将opener安装为全局
        urllib.request.install_opener(opener)
        #data为对应博客列表页的所有博文的点击数与评论数数据
        data=urllib.request.urlopen(hcurl).read()
        #pat2为提取文章阅读数的正则表达式
        pat2="click\d*?','(\d*?)'"
        #pat3为提取文章评论数的正则表达式
        pat3="comment\d*?','(\d*?)'"
        #提取阅读数和评论数数据并分别赋值给item下的hits和comment
        item["hits"]=re.compile(pat2).findall(str(data))
        item["comment"]=re.compile(pat3).findall(str(data))
        yield item
        #提取博文列表页的总页数
        pat4="blog.hexun.com/p(.*?)/"
        #通过正则表达式获取到的数据为一个列表，倒数第二个元素为总页数
        data2=re.compile(pat4).findall(str(response.body))
        if(len(data2)>=2):
            totalurl=data2[-2]
        else:
            totalurl=1
        #在实际运行中，下一行print的代码可以注释掉，在调试过程中，可以开启下一行print的代码
        #print("一共"+str(totalurl)+"页")
        #进入for循环，依次爬取各博文列表页的博文数据
        for i in range(2,int(totalurl)+1):
            #构造下一次要爬取的url，爬取一下页博文列表页中的数据
            nexturl="http://"+str(self.uid)+".blog.hexun.com/p"+str(i)+"/default.html"
            #进行下一次爬取，下一次爬取仍然模拟成浏览器进行
            yield Request(nexturl,callback=self.parse,headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})
    













