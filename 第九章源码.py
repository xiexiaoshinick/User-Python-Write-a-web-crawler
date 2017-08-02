#第九章
#9.3 定向抓取实战
#（1）
import urllib.request
import http.cookiejar
import re
#视频编号
vid="1472528692"
#刚开始时候的评论ID
comid="6173403130078248384"
url= "http://coral.qq.com/article/"+vid+"/comment?commentid="+comid+"&reqnum=20"
headers={ "Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Encoding":" gb2312,utf-8",
                        "Accept-Language":" zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
                        "Connection": "keep-alive",
                        "referer":"qq.com"}
cjar=http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
headall=[]
for key,value in headers.items():
    item=(key,value)
    headall.append(item)
opener.addheaders = headall
urllib.request.install_opener(opener)
#建立一个自定义函数craw(vid,comid),实现自动抓取对应评论网页并返回抓取数据
def craw(vid,comid):
    url= "http://coral.qq.com/article/"+vid+"/comment?commentid="+comid+"&reqnum=20"
    data=urllib.request.urlopen(url).read().decode("utf-8")
    return data
idpat='"id":"(.*?)"'
userpat='"nick":"(.*?)",'
conpat='"content":"(.*?)",'
#第一层循环，代表抓取多少页，每一次外层循环抓取一页
for i in range(1,10):
    print("------------------------------------")
    print("第"+str(i)+"页评论内容")
    data=craw(vid,comid)
    #第二层循环，根据抓取的结果提取并处理每条评论的信息，一页20条评论
    for j in range(0,20):
        idlist=re.compile(idpat,re.S).findall(data)
        userlist=re.compile(userpat,re.S).findall(data)
        conlist=re.compile(conpat,re.S).findall(data)
        print("用户名是 :"+eval('u"'+userlist[j]+'"'))
        print("评论内容是:"+eval('u"'+conlist[j]+'"'))
        print("\n")
    #将comid改变为该页的最后一条评论id，实现不断自动加载
    comid=idlist[19]


