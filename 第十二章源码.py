#第十二章
#12.3 常用工具命令
#(1)
from scrapy.spiders import Spider
 
class FirstSpider(Spider):
    name = "first"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://www.baidu.com",
    ]
 
    def parse(self, response):
        pass

#(2)
>>> ti=sel.xpath("/html/head/title")
>>> print(ti)
[<Selector xpath='/html/head/title' data='<title>百度一下，你就知道</title>'>]
>>> 

#(3)
>>> exit()
D:\Python35\myweb\part12>

#12.4 实战Items
#(1)
class MyfirstpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    urlname=scrapy.Field()
    urlkey=scrapy.Field()
    urlcr=scrapy.Field()
    urladdr=scrapy.Field()

#(2)
>>> import scrapy
>>> class person(scrapy.Item):
	name=scrapy.Field()
	job=scrapy.Field()
	email=scrapy.Field()
#(3)
>>> weisuen=person(name="weiwei",job="teacher",email="qiansyy@iqianyue.com")

#(4)
>>> print(weisuen)
{'email': 'qiansyy@iqianyue.com', 'job': 'teacher', 'name': 'weiwei'}

#(5)
>>> weisuen["job"]
'teacher'

#(6)
>>> weisuen["email"]
'abc@sina.com'

#(7)
>>> weisuen.keys()
dict_keys(['job', 'email', 'name'])

#(8)
>>> weisuen.items()
ItemsView({'email': 'abc@sina.com', 'job': 'teacher', 'name': 'weiwei'})

#12.5 实战Spider类
#(1)
# -*- coding: utf-8 -*-
import scrapy
from myfirstpjt.items import MyfirstpjtItem

class WeisuenSpider(scrapy.Spider):
    name = "weisuen"
    allowed_domains = ["sina.com.cn"]
    start_urls = (
        'http://slide.news.sina.com.cn/s/slide_1_2841_103185.html',
        'http://slide.mil.news.sina.com.cn/k/slide_8_193_45192.html#p=1',
        'http://news.sina.com.cn/pl/2016-09-12/doc-ifxvukhv8147404.shtml',
    )

    def parse(self, response):
        item=MyfirstpjtItem()
        item["urlname"]=response.xpath("/html/head/title/text()")
        print(item["urlname"])

#(2)
# -*- coding: utf-8 -*-
import scrapy
from myfirstpjt.items import MyfirstpjtItem

class WeisuenSpider(scrapy.Spider):
    name = "weisuen"
    start_urls = (
        'http://slide.news.sina.com.cn/s/slide_1_2841_103185.html',
        'http://slide.mil.news.sina.com.cn/k/slide_8_193_45192.html#p=1',
        'http://news.sina.com.cn/pl/2016-09-12/doc-ifxvukhv8147404.shtml',
    )
#定义了新属性url2
    urls2=("http://www.jd.com",
           "http://sina.com.cn",
           "http://yum.iqianyue.com",
           )
#重写了start_requests()方法
    def start_requests(self):
#在该方法中将起始网址设置为从新属性url2中读取
        for url in self.urls2:
#调用默认make_requests_from_url()方法生成具体请求并通过yield返回
            yield self.make_requests_from_url(url)
    def parse(self, response):
        item=MyfirstpjtItem()
        item["urlname"]=response.xpath("/html/head/title/text()")
        print(item["urlname"])

#12.7 	Spider类参数传递
#(1)
# -*- coding: utf-8 -*-
import scrapy
from myfirstpjt.items import MyfirstpjtItem

class WeisuenSpider(scrapy.Spider):
    name = "weisuen"
#此时虽然还在此定义了start_urls属性，但不起作用，因为在构造方法进行了重写
    start_urls = (
        'http://slide.news.sina.com.cn/s/slide_1_2841_103185.html',
        'http://slide.mil.news.sina.com.cn/k/slide_8_193_45192.html#p=1',
        'http://news.sina.com.cn/pl/2016-09-12/doc-ifxvukhv8147404.shtml',
    )
#重写初始化方法__init__()，并设置参数myurl
    def __init__(self,myurl=None,*args,**kwargs):
        super(WeisuenSpider,self).__init__(*args,**kwargs)
#输出要爬的网址，对应值为接收到的参数
        print("要爬取的网址为：%s"%myurl)
#重新定义start_urls属性，属性值为传进来的参数值
        self.start_urls=["%s"%myurl]
    def parse(self, response):
        item=MyfirstpjtItem()
        item["urlname"]=response.xpath("/html/head/title/text()")
        print("以下将显示爬取的网址的标题")
        print(item["urlname"])

#(2)
# -*- coding: utf-8 -*-
import scrapy
from myfirstpjt.items import MyfirstpjtItem

class WeisuenSpider(scrapy.Spider):
    name = "weisuen"

    start_urls = (
        'http://slide.news.sina.com.cn/s/slide_1_2841_103185.html',
        'http://slide.mil.news.sina.com.cn/k/slide_8_193_45192.html#p=1',
        'http://news.sina.com.cn/pl/2016-09-12/doc-ifxvukhv8147404.shtml',
    )

    def __init__(self,myurl=None,*args,**kwargs):
        super(WeisuenSpider,self).__init__(*args,**kwargs)
#通过split()将传递进来的参数以“|”为切割符进行分隔，分隔后生成一个列表并赋值给myurllist变量
        myurllist=myurl.split("|")
#通过for循环遍历该列表myurllist，并分别输出传进来要爬取的各网址
        for i in myurllist:
            print("要爬取的网址为：%s"%i)
#将起始网址设置为传进来的参数中各网址组成的列表
        self.start_urls=myurllist
    def parse(self, response):
        item=MyfirstpjtItem()
        item["urlname"]=response.xpath("/html/head/title/text()")
        print("以下将显示爬取的网址的标题")
        print(item["urlname"])

#12.8 用XMLFeedSpider来分析XML源
#(1)
D:\Python35\myweb\part12>scrapy startproject myxml
New Scrapy project 'myxml', using template directory 'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\Python35\myweb\part12\myxml

You can start your first spider with:
    cd myxml
    scrapy genspider example example.com

#(2)
import scrapy
class MyxmlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#存储文章标题
    title=scrapy.Field()
#存储对应链接
    link=scrapy.Field()
#存储对应文章作者
    author=scrapy.Field()
定义好要存储的结构化数据之后，可以创建一个爬虫文件用于分析XML源，如下所示。
D:\Python35\myweb\part12>cd myxml\
D:\Python35\myweb\part12\myxml>scrapy genspider -l
Available templates:
  basic
  crawl
  csvfeed
  xmlfeed
D:\Python35\myweb\part12\myxml>scrapy genspider -t xmlfeed myxmlspider sina.com.cn
Created spider 'myxmlspider' using template 'xmlfeed' in module:
  myxml.spiders.myxmlspider

#(3)
# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from myxml.items import MyxmlItem
class MyxmlspiderSpider(XMLFeedSpider):
    name = 'myxmlspider'
    allowed_domains = ['sina.com.cn']
#设置要分析的XML文件地址
    start_urls = ['http://blog.sina.com.cn/rss/1615888477.xml']
    iterator = 'iternodes' # you can change this; see the docs
#此时将开始迭代的节点设置为第一个节点rss
    itertag = 'rss' # change it accordingly
    def parse_node(self, response, node):
        i = MyxmlItem()
#利用XPath表达式将对应信息提取出来，并存储到对应的Item中
        i['title'] = node.xpath("/rss/channel/item/title/text()").extract()
        i['link'] = node.xpath("/rss/channel/item/link/text()").extract()
        i['author'] = node.xpath("/rss/channel/item/author/text()").extract()
#通过for循环以此遍历出提取出来存在item中的信息并输出
        for j in range(len(i['title'])):
            print("第"+str(j+1)+"篇文章")
            print("标题是：")
            print(i['title'][j])
            print("对应链接是：")
            print(i['link'][j])
            print("对应作者是：")
            print(i['author'][j])
            print("----------------------")
        return i

#(4)
D:\Python35\myweb\part12\myxml>scrapy genspider -t xmlfeed person iqianyue.com
Created spider 'person' using template 'xmlfeed' in module:
  myxml.spiders.person

#(5)
# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from myxml.items import MyxmlItem
class PersonSpider(XMLFeedSpider):
    name = 'person'
    allowed_domains = ['iqianyue.com']
#设置XML网址
    start_urls = ['http://yum.iqianyue.com/weisuenbook/pyspd/part12/test.xml']
    iterator = 'iternodes' # you can change this; see the docs
#设置开始迭代的节点
    itertag = 'person' # change it accordingly

    def parse_node(self, response, selector):
        i = MyxmlItem()
#提取邮件信息
        i['link'] = selector.xpath('/person/email/text()').extract()
#输出提取到的邮件信息
        print(i['link'])
        return i

#12.9 学会使用CSVFeedSpider
#(1)
D:\Python35\myweb\part12>scrapy startproject mycsv
New Scrapy project 'mycsv', using template directory 'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\Python35\myweb\part12\mycsv

You can start your first spider with:
    cd mycsv
    scrapy genspider example example.com

#(2)
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
import scrapy
class MycsvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    sex=scrapy.Field()

#(3)
D:\Python35\myweb\part12\mycsv>scrapy genspider -t csvfeed mycsvspider iqianyue.com
Created spider 'mycsvspider' using template 'csvfeed' in module:
  mycsv.spiders.mycsvspider

#(4)
# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider
from mycsv.items import MycsvItem
class MycsvspiderSpider(CSVFeedSpider):
    name = 'mycsvspider'
    allowed_domains = ['iqianyue.com']
#定义要处理的csv文件所在的网址
    start_urls = ['http://yum.iqianyue.com/weisuenbook/pyspd/part12/mydata.csv']
#定义headers
    headers = ['name', 'sex','addr','email']
    #定义间隔符
delimiter = ','
    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response
    def parse_row(self, response, row):
        i = MycsvItem()
#提取各行的name这一列的信息
        i['name'] = row['name'].encode()
#提取各行的sex这一列的信息
        i['sex'] = row['sex'].encode()
#进行信息输出
        print("名字是：")
        print(i['name'])
        print("性别是：")
        print(i['sex'])
#输出完一个记录的对应列的信息后，输出一个间隔符，显示起来方便观察
        print("--------------------")
        return i
    
#12.10  Scrapy爬虫多开技能
#(1)
D:\Python35\myweb\part12>scrapy startproject mymultispd
New Scrapy project 'mymultispd', using template directory 'd:\\python35\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\Python35\myweb\part12\mymultispd

You can start your first spider with:
    cd mymultispd
    scrapy genspider example example.com

#(2)
D:\Python35\myweb\part12>cd mymultispd

D:\Python35\myweb\part12\mymultispd>scrapy genspider -t basic myspd1 sina.com.cn
Created spider 'myspd1' using template 'basic' in module:
  mymultispd.spiders.myspd1

D:\Python35\myweb\part12\mymultispd>scrapy genspider -t basic myspd2 sina.com.cn
Created spider 'myspd2' using template 'basic' in module:
  mymultispd.spiders.myspd2

D:\Python35\myweb\part12\mymultispd>scrapy genspider -t basic myspd3 sina.com.cn
Created spider 'myspd3' using template 'basic' in module:
  mymultispd.spiders.myspd3

#(3)
import os
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.python import without_none_values
from scrapy.exceptions import UsageError


class Command(ScrapyCommand):
    requires_project = True
    def syntax(self):
        return "[options] <spider>"
    def short_desc(self):
#命令描述信息，可以根据个人喜好适当修改一下
        return "Run all spider"
    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")
    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
        if opts.output:
            if opts.output == '-':
                self.settings.set('FEED_URI', 'stdout:', priority='cmdline')
            else:
                self.settings.set('FEED_URI', opts.output, priority='cmdline')
            feed_exporters = without_none_values(
                self.settings.getwithbase('FEED_EXPORTERS'))
            valid_output_formats = feed_exporters.keys()
            if not opts.output_format:
                opts.output_format = os.path.splitext(opts.output)[1].replace(".", "")
            if opts.output_format not in valid_output_formats:
                raise UsageError("Unrecognized output format '%s', set one"
                                 " using the '-t' switch or as a file extension"
                                 " from the supported list %s" % (opts.output_format,
                                                                  tuple(valid_output_formats)))
            self.settings.set('FEED_FORMAT', opts.output_format, priority='cmdline')
    #主要修改这里
    def run(self, args, opts):
        #获取爬虫列表
        spd_loader_list=self.crawler_process.spider_loader.list()
        #遍历各爬虫
        for spname in spd_loader_list or args:
            self.crawler_process.crawl(spname, **opts.spargs)
            print("此时启动的爬虫为："+spname)
        self.crawler_process.start()

#12.11 避免被ban
#(1)
# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.7

#(2)
#IP池设置
IPPOOL=[
    {"ipaddr":"121.33.226.167:3128"},
    {"ipaddr":"118.187.10.11:80"},
    {"ipaddr":"123.56.245.138:808"},
    {"ipaddr":"139.196.108.68:80"},
    {"ipaddr":"36.250.87.88:47800"},
    {"ipaddr":"123.57.190.51:7777"},
    {"ipaddr":"171.39.26.176:8123"}
]

#(3)
#middlewares下载中间件
#导入随机数模块，目的是随机挑选一个IP池中的ip
import random
#从settings文件（myfirstpjt.settings为settings文件的地址）中导入设置好的IPPOOL
from myfirstpjt.settings import IPPOOL
#导入官方文档中HttpProxyMiddleware对应的模块
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware

class IPPOOLS(HttpProxyMiddleware):
#初始化方法
    def __init__(self,ip=''):
        self.ip=ip
#process_request()方法，主要进行请求处理
    def process_request(self,request,spider):
#先随机选择一个IP
        thisip=random.choice(IPPOOL)
#输出当前选择的IP，便于调试观察
        print("当前使用的IP是："+thisip["ipaddr"])
#将对应的IP实际添加为具体的代理，用该IP进行爬取
        request.meta["proxy"]="http://"+thisip["ipaddr"]

#(4)
DOWNLOADER_MIDDLEWARES = {
    #'myfirstpjt.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':123,
    'myfirstpjt.middlewares.IPPOOLS':125
}

#(5)
#用户代理（user-agent）池设置
UAPOOL=[
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5"
]

#(6)
#uamid下载中间件
import random
from myfirstpjt.settings import UAPOOL
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

class Uamid(UserAgentMiddleware):
    def __init__(self,ua=''):
        self.ua=ua
    def process_request(self,request,spider):
        thisua=random.choice(UAPOOL)
        print("当前使用的user-agent是："+thisua)
        request.headers.setdefault('User-Agent',thisua)

#(7)
# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'myfirstpjt.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware':2,
    'myfirstpjt.uamid.Uamid':1
}

