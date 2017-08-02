#第四章
#4.2  快速使用Urllib扒取网页
#(1)
>>> import urllib.request

#(2)
>>> file=urllib.request.urlopen("http://www.baidu.com")

#(3)
>>> data=file.read()
>>> dataline=file.readline()

#(4)
>>> print(dataline)

#(5)
>>> print(data)

#(6)
>>> fhandle=open("D:/Python35/myweb/part4/1.html","wb")
>>> fhandle.write(data)
99437
>>> fhandle.close()

#(7)
>>>filename=urllib.request.urlretrieve("http://edu.51cto.com",filename="D:/Python35/myweb/part4/2.html")

#(8)
>>> urllib.request.urlcleanup()

#(9)
>>> file.info()
<http.client.HTTPMessage object at 0x0000000003623D68>

#(10)
>>> file.getcode()
200

#(11)
>>> file.geturl()
'http://www.baidu.com'

#(12)
>>> urllib.request.quote("http://www.sina.com.cn")
'http%3A//www.sina.com.cn'

#(13)
>>> urllib.request.unquote("http%3A//www.sina.com.cn")
'http://www.sina.com.cn'

#4.3  浏览器的完全模拟--Headers属性
#(1)
>>> import urllib.request
>>> url= "http://blog.csdn.net/weiwei_pig/article/details/51178226"
>>> file=urllib.request.urlopen(url)

#(2)
mport urllib.request
url= "http://blog.csdn.net/weiwei_pig/article/details/51178226"
headers=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
data=opener.open(url).read()

#(3)
>>> fhandle=open("D:/Python35/myweb/part4/3.html","wb")
>>> fhandle.write(data)
47630
>>> fhandle.close()

#(4)
import urllib.request
url= "http://blog.csdn.net/weiwei_pig/article/details/51178226"
req=urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
data=urllib.request.urlopen(req).read()

#4.4  超时设置
#(1)
import urllib.request
for i in range(1,100):
    try:
        file=urllib.request.urlopen("http://yum.iqianyue.com",timeout=1)
        data=file.read()
        print(len(data))
    except Exception as e:
        print("出现异常-->"+str(e))
#(2)
import urllib.request
for i in range(1,100):
    try:
        file=urllib.request.urlopen("http://yum.iqianyue.com",timeout=30)
        data=file.read()
        print(len(data))
    except Exception as e:
        print("出现异常-->"+str(e))

#4.5  HTTP协议请求实战
#(1)
mport urllib.request
keywd="hello"
url="http://www.baidu.com/s?wd="+keywd
req=urllib.request.Request(url)
data=urllib.request.urlopen(req).read()
fhandle=open("D:/Python35/myweb/part4/4.html","wb")
fhandle.write(data)
fhandle.close()

#(2)
import urllib.request
url="http://www.baidu.com/s?wd="
key="韦玮老师"
key_code=urllib.request.quote(key)
url_all=url+key_code
req=urllib.request.Request(url_all)
data=urllib.request.urlopen(req).read()
fh=open("D:/Python35/myweb/part4/5.html","wb")
fh.write(data)
fh.close()

#(3)
import urllib.request
import urllib.parse
url = "http://www.iqianyue.com/mypost/"
postdata =urllib.parse.urlencode({
"name":"ceo@iqianyue.com",
"pass":"aA123456"
}).encode('utf-8') #将数据使用urlencode编码处理后，使用encode()设置为utf-8编码
req = urllib.request.Request(url,postdata)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
data=urllib.request.urlopen(req).read()
fhandle=open("D:/Python35/myweb/part4/6.html","wb")
fhandle.write(data)
fhandle.close()

#4.6  瞒天过海之代理服务器的设置
#(1)
def use_proxy(proxy_addr,url):
    import urllib.request
    proxy= urllib.request.ProxyHandler({'http':proxy_addr})  
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)  
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf-8')
    return data
proxy_addr="202.75.210.45:7777"
data=use_proxy(proxy_addr,"http://www.baidu.com")
print(len(data))

#4.7  DebugLog实战
#(1)
import urllib.request
httphd=urllib.request.HTTPHandler(debuglevel=1)
httpshd=urllib.request.HTTPSHandler(debuglevel=1)
opener=urllib.request.build_opener(httphd,httpshd)
urllib.request.install_opener(opener)
data=urllib.request.urlopen("http://edu.51cto.com")

#4.8  异常处理神器--URLError实战
#(1)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.URLError as e:
    print(e.code)
    print(e.reason)

#(2)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)

#(3)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.baidusss.net")
except urllib.error.HTTPError as e:
    print(e.reason)

#(4)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.baidusss.net")
except urllib.error.URLError as e:
    print(e.reason)

#(5)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.baidusss.net")
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)
except urllib.error.URLError as e:
    print(e.reason)

#(6)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://www.baidussssss.net")
except urllib.error.URLError as e:
    print(e.code)
    print(e.reason)

#(7)
import urllib.request
import urllib.error
try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.URLError as e:
    if hasattr(e,"code"):
        print(e.code)
    if hasattr(e,"reason"):
        print(e.reason)

