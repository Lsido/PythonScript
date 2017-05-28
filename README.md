# News.py

基于Python2.7写的单线程爬搜狐新闻列表批量存入数据库

新闻列表：http://wei.sohu.com/roll/ 大概900个页码，每页40*900 约36000篇新闻

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
