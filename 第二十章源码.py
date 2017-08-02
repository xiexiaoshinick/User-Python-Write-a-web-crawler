#第20章模拟登录爬虫项目
#20.3 模拟登录爬虫项目编写实战
#(1)
# -*- coding: utf-8 -*-
import scrapy
import urllib.request
from scrapy.http import Request,FormRequest


class LoginspdSpider(scrapy.Spider):
    name = "loginspd"
    allowed_domains = ["douban.com"]
    #设置头信息变量，供下面的代码中模拟成浏览器爬取
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
    #编写start_requests()方法，第一次会默认调取该方法中的请求
    def start_requests(self):
        #首先爬一次登录页，然后进入回调函数parse()
        return [Request("https://accounts.douban.com/login", meta={"cookiejar": 1}, callback=self.parse)]

    def parse(self, response):
        #获取验证码图片所在地址，获取后赋给captcha变量，此时captcha为一个列表
        captcha=response.xpath('//img[@id="captcha_image"]/@src').extract()
        #因为登录时有时网页有验证码，有时网页没有验证码
        # 所以需要判断此时是否需要输入验证码，若captcha列表中有元素，说明有验证码信息
        if len(captcha)>0:
            print("此时有验证码")
            #设置将验证码图片存储到本地的本地地址
            localpath="D:/Python35/myweb/part20/loginpjt/captcha.png"
            #将服务器中的验证码图片存储到本地，供我们在本地直接进行查看
            urllib.request.urlretrieve(captcha[0], filename=localpath)
            print("请查看本地图片captcha.png并输入对应验证码：")
            #通过input()等待我们输入对应的验证码并赋给captcha_value变量
            captcha_value=input()
            #设置要传递的post信息
            data={
                #设置登录账号，格式为账号字段名:具体账号
                "form_email":"weisuen007@163.com",
                #设置登录密码，格式为密码字段名:具体密码，读者需要将账号密码换成自己的
                #因为笔者完成该项目后已经修改密码
                "form_password":"weijc7789",
                #设置验证码，格式为验证码字段名:具体验证码
                "captcha-solution":captcha_value,
                #设置需要转向的网址，由于我们需要爬取个人中心页，所以转向个人中心页
                "redir":"https://www.douban.com/people/151968962/",
            }
        #否则说明captcha列表中没有元素，即此时不需要输入验证码信息
        else:
            print("此时没有验证码")
            #设置要传递的post信息，此时没有验证码字段
            data={
                "form_email":"weisuen007@163.com",
                "form_password":"weijc7789",
                "redir": "https://www.douban.com/people/151968962/",
            }
        print("登录中…")
        #通过FormRequest.from_response()进行登录
        return [FormRequest.from_response(response,
                                          #设置cookie信息
                                          meta={"cookiejar": response.meta["cookiejar"]},
                                          #设置headers信息模拟成浏览器
                                          headers=self.header,
                                          #设置post表单中的数据
                                          formdata=data,
                                          #设置回调函数，此时回调函数为next()
                                          callback=self.next,
                                          )]
    def next(self,response):
        print("此时已经登录完成并爬取了个人中心的数据")
        #此时response为个人中心网页中的数据
        #以下通过Xpath表达式分别提取个人中心中该用户的相关信息
        #网页标题Xpath表达式
        xtitle="/html/head/title/text()"
        #日记标题Xpath表达式
        xnotetitle="//div[@class='note-header pl2']/a/@title"
        #日记发表时间Xpath表达式
        xnotetime="//div[@class='note-header pl2']//span[@class='pl']/text()"
        #日记内容Xpath表达式
        xnotecontent="//div[@class='mbtr2']/div[@class='note']/text()"
        #日记链接Xpath表达式
        xnoteurl="//div[@class='note-header pl2']/a/@href"

        #分别提取网页标题、日记标题、日记发表时间、日记内容、日记链接
        title=response.xpath(xtitle).extract()
        notetitle = response.xpath(xnotetitle).extract()
        notetime = response.xpath(xnotetime).extract()
        notecontent = response.xpath(xnotecontent).extract()
        noteurl = response.xpath(xnoteurl).extract()
        print("网页标题是："+title[0])
        #可能有多篇日记，通过for循环依次遍历
        for i in range(0,len(notetitle)):
            print("第"+str(i+1)+"篇文章的信息如下:")
            print("文章标题为："+notetitle[i])
            print("文章发表时间为：" + notetime[i])
            print("文章内容为：" + notecontent[i])
            print("文章链接为：" + noteurl[i])




            
            print("------------")
