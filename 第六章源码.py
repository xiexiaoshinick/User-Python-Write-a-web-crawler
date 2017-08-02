#第六章
#6.1 简单Python爬虫的实现
#(1)
<img width="220" height="220" data-img="1" data-lazy-img="//img12.360buyimg.com/n7/jfs/t2437/118/775474476/74776/4087862f/562616d9Nc17cd80a.jpg">
图片2对应代码：
<img width="220" height="220" data-img="1" data-lazy-img="//img10.360buyimg.com/n7/jfs/t2230/83/2893465811/162158/80a547ef/56fa0f30N7794db4a.jpg">

#(2)
import re
import urllib.request
def craw(url,page):
    html1=urllib.request.urlopen(url).read()
    html1=str(html1)
    pat1='<div id="plist".+? <div class="page clearfix">'
    result1=re.compile(pat1).findall(html1)
    result1=result1[0]
    pat2='<img width="220" height="220" data-img="1" data-lazy-img="//(.+?\.jpg)">'
    imagelist=re.compile(pat2).findall(result1)
    x=1
    for imageurl in imagelist:
        imagename="D:/Python35/myweb/part6/img1/"+str(page)+str(x)+".jpg"
        imageurl="http://"+imageurl
        try:
            urllib.request.urlretrieve(imageurl,filename=imagename)
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                x+=1
            if hasattr(e,"reason"):
                x+=1
        x+=1

#6.2 抓取页面链接实战
#(1)
#抓取页面链接
import re
import urllib.request
def getlink(url):
    #模拟成浏览器
    headers=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    #将opener安装为全局
    urllib.request.install_opener(opener)
    file=urllib.request.urlopen(url)
    data=str(file.read())
    #根据需求构建好链接表达式
    pat='(https?://[^\s)";]+\.(\w|/)*)' 
    link=re.compile(pat).findall(data)
    #去除重复元素
    link=list(set(link))
    return link
#要爬取的网页链接
url="http://blog.csdn.net/"
#获取对应网页中包含的链接地址
linklist=getlink(url)
#通过for循环分别遍历输出获取到的链接地址到屏幕上
for link in linklist:
    print(link[0])
    
#(2)
import urllib.request
import re
def getcontent(url,page):
    #模拟成浏览器
    headers=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    #将opener安装为全局
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(url).read().decode("utf-8")
    #构建对应用户提取的正则表达式
    userpat='target="_blank" title="(.*?)">'
    #构建段子内容提取的正则表达式
    contentpat='<div class="content">(.*?)</div>'
    #寻找出所有的用户
    userlist=re.compile(userpat,re.S).findall(data)
    #寻找出所有的内容
    contentlist=re.compile(contentpat,re.S).findall(data)
    x=1
    #通过for循环遍历段子内容并将内容分别赋给对应的变量
    for content in contentlist:
        content=content.replace("\n","")
        #用字符串作为变量名，先将对应字符串赋给一个变量
        name="content"+str(x)
         #通过exec()函数实现用字符串作为变量名并赋值
        exec(name+'=content')
        x+=1
    y=1
    #通过for循环遍历用户，并输出该用户对应的内容
    for user in userlist:
        name="content"+str(y)
        print("用户"+str(page)+str(y)+"是:"+user)
        print("内容是:")
        exec("print("+name+")")
        print("\n")
        y+=1
#分别获取各页的段子，通过for循环可以获取多页
for i in range(1,30):
    url="http://www.qiushibaike.com/8hr/page/"+str(i)
    getcontent(url,i)

#6.4 微信爬虫实战
#(1)
import re
import urllib.request
import time
import urllib.error
#模拟成浏览器
headers=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
#将opener安装为全局
urllib.request.install_opener(opener)
#设置一个列表listurl存储文章网址列表
listurl=[]
#自定义函数，功能为使用代理服务器
def use_proxy(proxy_addr,url):
    #建立异常处理机制
    try:
        import urllib.request
        proxy= urllib.request.ProxyHandler({'http':proxy_addr})  
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)  
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        #若为URLError异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        print("exception:"+str(e))
        #若为Exception异常，延时1秒执行
        time.sleep(1)
#获取所有文章链接
def getlisturl(key,pagestart,pageend,proxy):
    try:
        page=pagestart
        #编码关键词key
        keycode=urllib.request.quote(key)
        #编码"&page"
        pagecode=urllib.request.quote("&page")
        #循环爬取各页的文章链接
        for page in range(pagestart,pageend+1):
            #分别构建各页的url链接，每次循环构建一次
            url="http://weixin.sogou.com/weixin?type=2&query="+keycode+pagecode+str(page)
            #用代理服务器爬，解决IP被封杀问题
            data1=use_proxy(proxy,url)
            #获取文章链接的正则表达式
            listurlpat='<div class="txt-box">.*?(http://.*?)"'
            #获取每页的所有文章链接并添加到列表listurl中
            listurl.append(re.compile(listurlpat,re.S).findall(data1))
        print("共获取到"+str(len(listurl))+"页") #便于调试
        return listurl
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        #若为URLError异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        print("exception:"+str(e))
        #若为Exception异常，延时1秒执行
        time.sleep(1)
#通过文章链接获取对应内容
def getcontent(listurl,proxy):
    i=0
    #设置本地文件中的开始html编码
    html1='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>微信文章页面</title>
    </head>
    <body>'''
    fh=open("D:/Python35/myweb/part6/1.html","wb")
    fh.write(html1.encode("utf-8"))
    fh.close()
    #再次以追加写入的方式打开文件，以写入对应文章内容
    fh=open("D:/Python35/myweb/part6/1.html","ab")
    #此时listurl为二维列表，形如listurl[][],第一维存储的信息跟第几页相关，第二维存的跟该页第几个文章链接相关
    for i in range(0,len(listurl)):
        for j in range(0,len(listurl[i])):
            try:
                url=listurl[i][j]
                #处理成真实url，读者亦可以观察对应网址的关系自行分析，采集网址比真实网址多了一串amp
                url=url.replace("amp;","")
                #使用代理去爬取对应网址的内容
                data=use_proxy(proxy,url)
                #文章标题正则表达式
                titlepat="<title>(.*?)</title>"
                #文章内容正则表达式
                contentpat='id="js_content">(.*?)id="js_sg_bar"'
                #通过对应正则表达式找到标题并赋给列表title
                title=re.compile(titlepat).findall(data)
                #通过对应正则表达式找到内容并赋给列表content
                content=re.compile(contentpat,re.S).findall(data)
                #初始化标题与内容
                thistitle="此次没有获取到"
                thiscontent="此次没有获取到"
                #如果标题列表不为空，说明找到了标题，取列表第零个元素，即此次标题赋给变量thistitle
                if(title!=[]):
                    thistitle=title[0]
                if(content!=[]):
                    thiscontent=content[0]
                #将标题与内容汇总赋给变量dataall
                dataall="<p>标题为:"+thistitle+"</p><p>内容为:"+thiscontent+"</p><br>"
                #将该篇文章的标题与内容的总信息写入对应文件
                fh.write(dataall.encode("utf-8"))
                print("第"+str(i)+"个网页第"+str(j)+"次处理") #便于调试
            except urllib.error.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
                #若为URLError异常，延时10秒执行
                time.sleep(10)
            except Exception as e:
                print("exception:"+str(e))
                #若为Exception异常，延时1秒执行
                time.sleep(1)
    fh.close()
    #设置并写入本地文件的html后面结束部分代码
    html2='''</body>
    </html>
    '''
    fh=open("D:/Python35/myweb/part6/1.html","ab")
    fh.write(html2.encode("utf-8"))
    fh.close()
#设置关键词            
key="物联网"
#设置代理服务器，该代理服务器有可能失效，读者需要换成新的有效代理服务器
proxy="119.6.136.122:80"
#可以为getlisturl()与getcontent()设置不同的代理服务器，此处没有启用该项设置
proxy2=""
#起始页
pagestart=1
#抓取到哪页
pageend=2
listurl=getlisturl(key,pagestart,pageend,proxy)
getcontent(listurl,proxy)

#6.6 多线程爬虫实战
#(1)
#多线程基础
import threading
class A(threading.Thread):
    def __init__(self):
        #初始化该线程
        threading.Thread.__init__(self)
    def run(self):
        #该线程要执行的程序内容
        for i in range(10):
            print("我是线程A")
class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(10):
            print("我是线程B")
#实例化线程A为t1
t1=A()
#启动线程t1
t1.start()
#实例化线程B为t2
t2=B()
#启动线程t2，此时与t1同时执行
t2.start()

#(2)
import threading
import queue
import re
import urllib.request
import time
import urllib.error

urlqueue=queue.Queue()
#模拟成浏览器
headers=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
#将opener安装为全局
urllib.request.install_opener(opener)
listurl=[]
 #使用代理服务器的函数
def use_proxy(proxy_addr,url): 
    try:
        proxy= urllib.request.ProxyHandler({'http':proxy_addr})  
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)  
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        time.sleep(10)
    except Exception as e:
        print("exception:"+str(e))
        time.sleep(1)
#线程1，专门获取对应网址并处理为真实网址
class geturl(threading.Thread):
    def __init__(self,key,pagestart,pageend,proxy,urlqueue):
        threading.Thread.__init__(self)
        self.pagestart=pagestart
        self.pageend=pageend
        self.proxy=proxy
        self.urlqueue=urlqueue
        self.key=key
    def run(self):
        page=self.pagestart
        #编码关键词key
        keycode=urllib.request.quote(key)
        #编码"&page"
        pagecode=urllib.request.quote("&page")
        for page in range(self.pagestart,self.pageend+1):
            url="http://weixin.sogou.com/weixin?type=2&query="+keycode+pagecode+str(page)
            #用代理服务器爬，解决IP被封杀问题
            data1=use_proxy(self.proxy,url)
            #列表页url正则
            listurlpat='<div class="txt-box">.*?(http://.*?)"'
            listurl.append(re.compile(listurlpat,re.S).findall(data1))
        #便于调试
        print("获取到"+str(len(listurl))+"页") 
        for i in range(0,len(listurl)):
            #等一等线程2，合理分配资源
            time.sleep(7)
            for j in range(0,len(listurl[i])):
                try:
                    url=listurl[i][j]
                    #处理成真实url，读者亦可以观察对应网址的关系自行分析，采集网址比真实网址多了一串amp
                    url=url.replace("amp;","")
                    print("第"+str(i)+"i"+str(j)+"j次入队")
                    self.urlqueue.put(url)
                    self.urlqueue.task_done()
                except urllib.error.URLError as e:
                    if hasattr(e,"code"):
                        print(e.code)
                    if hasattr(e,"reason"):
                        print(e.reason)
                    time.sleep(10)
                except Exception as e:
                    print("exception:"+str(e))
                    time.sleep(1)
#线程2，与线程1并行执行，从线程1提供的文章网址中依次爬取对应文章信息并处理
class getcontent(threading.Thread):
    def __init__(self,urlqueue,proxy):
        threading.Thread.__init__(self)
        self.urlqueue=urlqueue
        self.proxy=proxy
    def run(self):
        html1='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>微信文章页面</title>
        </head>
        <body>'''
        fh=open("D:/Python35/myweb/part6/2.html","wb")
        fh.write(html1.encode("utf-8"))
        fh.close()
        fh=open("D:/Python35/myweb/part6/2.html","ab")
        i=1
        while(True):
            try:
                url=self.urlqueue.get()
                data=use_proxy(self.proxy,url)
                titlepat="<title>(.*?)</title>"
                contentpat='id="js_content">(.*?)id="js_sg_bar"'
                title=re.compile(titlepat).findall(data)
                content=re.compile(contentpat,re.S).findall(data)
                thistitle="此次没有获取到"
                thiscontent="此次没有获取到"
                if(title!=[]):
                     thistitle=title[0]
                if(content!=[]):
                      thiscontent=content[0]
                dataall="<p>标题为:"+thistitle+"</p><p>内容为:"+thiscontent+"</p><br>"
                fh.write(dataall.encode("utf-8"))
                print("第"+str(i)+"个网页处理") #便于调试
                i+=1
            except urllib.error.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
                time.sleep(10)
            except Exception as e:
                print("exception:"+str(e))
                time.sleep(1)
        fh.close()
        html2='''</body>
        </html>
        '''
        fh=open("D:/Python35/myweb/part6/2.html","ab")
        fh.write(html2.encode("utf-8"))
        fh.close()
#并行控制程序，若60秒未响应，并且存url的队列已空，则判断为执行成功
class conrl(threading.Thread):
    def __init__(self,urlqueue):
        threading.Thread.__init__(self)
        self.urlqueue=urlqueue
    def run(self):
        while(True):
            print("程序执行中")
            time.sleep(60)
            if(self.urlqueue.empty()):
                print("程序执行完毕！")
                exit()
key="人工智能"
proxy="119.6.136.122:80"
proxy2=""
pagestart=1#起始页
pageend=2#抓取到哪页
#创建线程1对象，随后启动线程1
t1=geturl(key,pagestart,pageend,proxy,urlqueue)
t1.start()
#创建线程2对象，随后启动线程2
t2=getcontent(urlqueue,proxy)
t2.start()
#创建线程3对象，随后启动线程3
t3=conrl(urlqueue)
t3.start()



for i in range(1,79):
    url="http://list.jd.com/list.html?cat=9987,653,655&page="+str(i)
    craw(url,i)

#(3)
