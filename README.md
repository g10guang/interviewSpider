# 命令行简单爬虫

## 需求

使用 Python 编写一个网站爬虫程序，支持参数如下：

```bash
spider.py -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number --dbfile  filepath  --key=”HTML5” -flush 10
```

**参数说明：**
+ -u 指定爬虫开始地址，需要指明完整的 url，如：http://g10guang.com/
+ -d 指定爬虫深度，默认为 5
+ --thread 指定线程池大小，多线程爬取页面，可选参数，默认10
+ --dbfile 存放结果数据到指定的数据库（sqlite）文件中，默认为 spider.db
+ --key 页面内的关键词，获取满足该关键词的网页，可选参数，默认为所有页面
+ -l 日志记录文件记录详细程度，数字越大记录越详细，可选参数，默认 spider.log
+ --testself 程序自测，可选参数，默认 False
+ -flush 刷新进度的间隔，以秒为单位，可选参数，默认 10

**功能描述：**
1. 指定网站爬取指定深度的页面，将包含指定关键词的页面内容存放到sqlite3数据库文件中
2. 程序每隔10秒在屏幕上打印进度信息
3. 支持线程池机制，并发爬取网页
4. 代码需要详尽的注释，自己需要深刻理解该程序所涉及到的各类知识点
5. 需要自己实现线程池

## 提示

+ 提示1：使用 re、urllib/urllib2、beautifulsoup/lxml2、threading、optparse、Queue、sqlite3、logger、doctest 等模块
+ 提示2：注意是“线程池”而不仅仅是多线程
+ 提示3：爬取 sina.com.cn 或其它你喜欢的目标网站，要求两级深度要能正常结束

建议程序可分阶段，逐步完成编写，例如：
+ 版本1：spider1.py -u url -d deep
+ 版本2：spider3.py -u url -d deep -f logfile -l loglevel(1-5)  --testself
+ 版本3：spider3.py -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number
+ 版本4：剩下所有功能
