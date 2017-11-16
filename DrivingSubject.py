# coding=utf-8
import requests
import re
from random import choice
import json
import random
from bs4 import BeautifulSoup
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#get请求
def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""
#异常处理数据库链接
try:
    conn = MySQLdb.connect(host='localhost',port= 3306,user = 'root',passwd='root',db='test',charset='utf8')
    cur = conn.cursor()
except Exception, e:
    print '发生了一个错误: %s, 你可以在这里删除错误的文档' % e

#python获取控制台参数
if sys.argv[1] == '小车':
    carType = 'car'
    chexing = 'C1C2C3C4'
elif sys.argv[1] == '货车':
    carType = 'truck'
    chexing = 'A2B2'
elif sys.argv[1] == '客车':
    carType = 'bus'
    chexing = 'A1A3B1'
elif sys.argv[1] == '摩托车':
    carType = 'moto'
    chexing = 'moto'
else:
    carType = 'car'
    chexing = 'C1C2C3C4'
kemu = sys.argv[2]
if sys.argv[2] == '科目一':
    r = getHTMLText('http://api2.jiakaobaodian.com/api/open/exercise/sequence.htm?_r=17801703702540802070&cityCode=511300&page=1&limit=25&course=kemu1&carType='+str(carType)+'&_=0.7121756361682074')
    pjson = json.loads(r)
    jlist = pjson['data']
else:
    r = getHTMLText('http://api2.jiakaobaodian.com/api/open/exercise/sequence.htm?_r=17801703702540802070&cityCode=511300&page=1&limit=25&course=kemu3&carType='+str(carType)+'&_=0.7121756361682074')
    pjson = json.loads(r)
    jlist = pjson['data']
a=0
data = jlist

#循环读取ID，从驾考宝典内获取单个id下的记录
for i in data:
    #各种异常傻瓜式处理
    try:
        problem = getHTMLText('http://api2.jiakaobaodian.com/api/open/question/question-list.htm?_r=19604815519963578102&page=1&limit=25&questionIds='+str(i))
        pjson = json.loads(problem)
        jlist = pjson['data']
    except:
        problem = getHTMLText('http://api2.jiakaobaodian.com/api/open/question/question-list.htm?_r=19604815519963578102&page=1&limit=25&questionIds='+str(i))
        pjson = json.loads(problem)
        jlist = pjson['data']

    if len(jlist) == 0:
        try:
            problem = getHTMLText('http://api2.jiakaobaodian.com/api/open/question/question-list.htm?_r=19604815519963578102&page=1&limit=25&questionIds='+str(i))
            pjson = json.loads(problem)
            jlist = pjson['data']
        except:
            problem = getHTMLText('http://api2.jiakaobaodian.com/api/open/question/question-list.htm?_r=19604815519963578102&page=1&limit=25&questionIds='+str(i))
            pjson = json.loads(problem)
            jlist = pjson['data']
    #异常处理获取某个题end

    #开始插入数据库
    for k in jlist:
        #数据库读取当前id题、判断数据库与驾考宝典是否一致，若无此题则插入本地数据库
        idCount=cur.execute("select * from yourtable where questionId = "+str(i))
        #如果上sql有记录，判断当前题目车型里是否含有当前车型，没有则将当前车型更新到当前题目，有则无动作
        CxCount=cur.execute("select * from yourtable where questionId = "+str(i)+" and chexing like '%"+str(chexing)+"%'")
        if idCount == 0:
        #if 1==1:
            if k['optionA'] == "正确":
                if k['answer'] == 32:
                    answer = "错误,"
                else:
                    answer = "正确,"
                try:
                    imgUrl = k['mediaContent']
                except:
                    imgUrl = '0'
                try:
                    explain = k['explain']
                except:
                    explain = '0'
                sql = "INSERT INTO `yourtable` (`chexing`, `kemu`, `zhangjieId`, `id`, `type`, `area1`, `area2`, `area3`, `area4`, `area5`, `region`, `title`, `content`, `imagesPath`, `musicPath`, `daan`, `score`, `tikuIndex`, `jieshi`, `beiyong`, `imagesWidth`, `imagesHeight`, `A`, `B`, `C`, `D`, `title2`, `xuanxiang2`, `changjingshifan1`, `changjingshifan2`,`questionId`) VALUES (%s, %s, '0', NULL, '判断题', NULL, NULL, NULL, NULL, NULL, NULL,%s, NULL, %s, NULL, %s, '1', '1', %s, '', NULL, NULL, NULL, NULL, NULL, NULL, '', '', '', '',%s);"
                reCount = cur.execute(sql,(chexing,kemu,k['question'],imgUrl,answer,explain,k['questionId']))
                conn.commit()
                print '判断题：'+str(k['question']) + '已插入数据库' 
            else:
                if k['answer'] == 16:
                    answer = "A,"
                elif k['answer'] == 32:
                    answer = "B,"
                elif k['answer'] == 64:
                    answer = "C,"
                else:
                    answer = "D,"
                try:
                    imgUrl = k['mediaContent']
                except:
                    imgUrl = "0"
                try:
                    explain = k['explain']
                except:
                    explain = '0'
                if k['optionType'] == 2:
                    atype = '多选题'
                else:
                    atype = '单选题'
                sql = "INSERT INTO `yourtable` (`chexing`, `kemu`, `zhangjieId`, `id`, `type`, `area1`, `area2`, `area3`, `area4`, `area5`, `region`, `title`, `content`, `imagesPath`, `musicPath`, `daan`, `score`, `tikuIndex`, `jieshi`, `beiyong`, `imagesWidth`, `imagesHeight`, `A`, `B`, `C`, `D`, `title2`, `xuanxiang2`, `changjingshifan1`, `changjingshifan2`,`questionId`) VALUES (%s, %s, '0', NULL, %s, NULL, NULL, NULL, NULL, NULL, NULL,%s, NULL, %s, NULL, %s, '1', '1', %s, '1', '1', '1', %s, %s, %s, %s, '', '', '', '', %s);"
                reCount = cur.execute(sql,(chexing,kemu,atype,k['question'],imgUrl,answer,explain,k['optionA'],k['optionB'],k['optionC'],k['optionD'],k['questionId']))
                conn.commit()
                
                print str(atype)+'：'+str(k['question']) + '已插入数据库'
        else:
             
            if CxCount == 1:
                print str(i)+':数据库已有当前题目'
            else:
                try:
                    sql = "update `yourtable` set chexing = CONCAT(`chexing`,'"+str(chexing)+"') where questionId = "+str(i)
                    reCount = cur.execute(sql)
                except:
                    sql = "update `yourtable` set chexing = CONCAT(`chexing`,'"+str(chexing)+"') where questionId = "+str(i)
                    reCount = cur.execute(sql)
    a=a+1
print "完成记录:"+str(a)
conn.commit()
cur.close()
conn.close()