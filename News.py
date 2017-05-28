# coding=utf-8 
#搜狐新闻爬虫 lsido.com
import requests
from bs4 import BeautifulSoup
import sys
import re
import MySQLdb
import json
reload(sys) 
sys.setdefaultencoding('utf8')
#获取新闻详情内容
def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = 'gbk'
        return r.text
    except:
        return ""

#解析新闻详情内容
def getContent(url):
    html = getHTMLText(url)
    # print(html)
    soup = BeautifulSoup(html,'lxml')
    title = soup.find_all(attrs={"itemprop": "headline"})
    #print(title[0].get_text())
    paras = soup.find_all(attrs={"itemprop": "articleBody"})
    [s.extract() for s in soup('script')] 
    [s.extract() for s in soup('style')] 
    [s.extract() for s in soup.select("div.new_hot1")] 
    soup.prettify()
    for para in paras:
        if len(para) > 0:
             return para
             
#遍历新闻列表,插入数据库
def getNewsList(url):
    
    wbdata = requests.get(url, timeout = 30)
    wbdata.raise_for_status()
    wbdata.encoding = 'gbk'
    soup = BeautifulSoup(wbdata.text,'html.parser')
    news_titles = soup.find_all(attrs={"test": "a"})
    acount = 0
    for n in news_titles:
        title = n.get_text()
        link = n.get("href")
        try:
            cont =  getContent(link)
            html_escaped = MySQLdb.escape_string(cont.encode('utf-8'))
            myc =  HttpPost(html_escaped)
        except Exception, e:
            print '发生了一个错误: %s, 你可以在这里删除错误的文档' % e
 
        try:  
             sql='你的sql语句'
             reCount = cur.execute(sql,(title,myc))
             conn.commit()  
        except Exception as e:  
            print e  
            conn.rollback()
        acount = acount+1  
        print('标题为:'+title+'-已成功插入数据库,总量:'+str(acount))
#生成新闻页码
def getNewsPage():
    page = range(940,944); 
    for n in reversed(page):
       n=n-1;
       url = 'http://wei.sohu.com/roll/index_' + str(n) + '.shtml'
       getNewsList(url)
       
#新闻伪原创（可加入至Python，但是性能有所降低，综合比较post本地php比加载Python快约20%，测试环境: MAC OS）
def HttpPost(content):
    url = 'http://localhost/words.php'
    d = {'content':content}
    r = requests.post(url, data=d)
    hjson = json.loads(r.text)
    return hjson['content']
#入口
def main():
     getNewsPage();

#数据库操作
conn = MySQLdb.connect(host='localhost',port= 3306,user = 'root',passwd='root',db='article',charset='utf8')
cur = conn.cursor()
main()
conn.commit()
cur.close()
conn.close()