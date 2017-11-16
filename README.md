# DrivingSubject.py

(2017.11.16)

基于Python2.7爬取驾考宝典所有题目爬虫

安装好拓展后，使用方法如下（控制台输入）:
```
python DrivingSubject.py 小车 科目一
```

加入更新判断,linux下可放入crontab定时执行,通过判断题目达到更新目的

具体看代码

备注:

驾考宝典获取题目ID接口:
```
http://api2.jiakaobaodian.com/api/open/question/list-by-tag.htm?_r=111922017237088616081&cityCode=511300&page=1&limit=25&course=kemu1&tagId=2&carType=car&_=0.5066246786512065
```

根据ID读取题目接口:
```
http://api2.jiakaobaodian.com/api/open/question/question-list.htm?_r=19604815519963578102&page=1&limit=25&questionIds=909400
```
返回Json如下:
![Image text](https://raw.githubusercontent.com/Lsido/PythonScript/master/images/ResJson.png)


# News.py

基于Python2.7写的单线程爬搜狐新闻列表批量存入数据库

新闻列表：http://wei.sohu.com/roll/ 大概100个页码，每页40*100 约4000篇新闻

使用需安装几个拓展
```
pip install requests
pip install BeautifulSoup
pip install bs4
pip install MySQL-python
```

其中新闻伪原创没加在Python里，可以自己定义进去
* 伪原创
PHP代码为：

```

function str_reWords($str)
{
    $words=array();
    $content = file_get_contents('词库.txt');
    $content = str_replace( "\r", "",$content);
    $content = preg_split('/\n/', $content, -1, PREG_SPLIT_NO_EMPTY);
    foreach($content as $k=>$v)
    {
        if($k!=0)
        {
            $str_data = explode('_',$v);
            $words+=array("$str_data[0]"=>"$str_data[1]");
        }
    }
    return strtr($str,$words);
}
die(json_encode(array ('content'=>str_reWords($_POST['content']))));




```
词库文件内容：
```
善良_善意
好人_不坏的人
```
Python将文章存入数据库时会转义HTML

PHP读取文章可使用函数stripslashes进行反转义：
```
	$content = str_replace('\n','',content); //替换换行
	$content = stripslashes($row['content']);//反转义 /
```

拓展：

可根据页面详情抓取{腾讯新闻}{百度新闻}{网易新闻}列表
