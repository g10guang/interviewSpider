#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-09 23:17
import argparse
import re


class ParseArgs:
    """
    解析命令行参数
    """

    def __init__(self):
        self.args = None
        self.err_msg = []
        self._parse()

    def _parse(self):
        """
        解析参数
        :return:
        """
        parser = argparse.ArgumentParser(description='网络爬虫')
        parser.add_argument('-u', dest='url', default='https://foofish.net/', metavar='http://g10guang.com', type=str, help='输入爬取的网站的 url')
        parser.add_argument('-f', dest='logfile', default='./log.txt', metavar='log.txt', type=str,
                            help='日志输出文件')
        parser.add_argument('-l', dest='loglevel', default=1, metavar='[1,5]', type=int, help='日志等级')
        parser.add_argument('--testself', dest='testself', action='store_const', const=True, default=False, help='自测试')
        parser.add_argument('-thread', dest='thread', default=10, metavar='10', type=int, help='线程池大小')
        parser.add_argument('-dbfile', dest='dbfile', metavar='./spider.db', default='spider.db', type=str,
                            help='sqlite3 数据保存文件')
        parser.add_argument('--key', dest='keyword', default='git', metavar='keyword', type=str, help='搜索关键字')
        parser.add_argument('-d', dest='depth', default=5, metavar='5', type=int, help='爬虫分析的深度')
        parser.add_argument('-flush', dest='flush', default=1, metavar='10', type=int, help='每个N秒刷新进度信息')
        self.args = parser.parse_args()
        self._validate()

    def _validate(self):
        """
        判断用户输入值是否合法
        :return:
        """
        self._validate_url()
        self._validate_logfile()
        self._validate_loglevel()
        self._validate_thread()
        self._validate_dbfile()
        self._validate_keyword()
        self._validate_depth()
        self._validate_flush()

    def _validate_url(self):
        """
        验证 url 是否正确
        :return:
        """
        url_pattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
        regexp = re.compile(url_pattern)
        if not regexp.match(self.args.url):
            self.err_msg.append('url {} is not the right format.'.format(self.args.url))

    def _validate_logfile(self):
        """
        验证 logfile 格式是否正确
        :return:
        """
        pass

    def _validate_loglevel(self):
        """
        验证 loglevel 格式是否正确
        :return:
        """
        if self.args.loglevel > 5 or self.args.loglevel < 1:
            self.err_msg.append('incorrect loglevel={} expected loglevel=[1,5]'.format(self.args.loglevel))

    def _validate_thread(self):
        """
        验证 thread 格式是否正确
        :return:
        """
        if self.args.thread <= 0:
            self.err_msg.append('incorrect thread={} expected thread>=1'.format(self.args.thread))

    def _validate_dbfile(self):
        """
        验证 dbfile 格式是否正确
        :return:
        """
        pass

    def _validate_keyword(self):
        """
        验证 keyword 格式是否正确
        :return:
        """

    def _validate_depth(self):
        """
        验证 depath 格式是否正确
        :return:
        """
        if self.args.depth < 0:
            self.err_msg.append('incorrect depth={} expected depth>=0'.format(self.args.depth))

    def _validate_flush(self):
        if self.args.flush <= 0:
            self.err_msg.append('incorrect flush={} expected flush>=1'.format(self.args.flush))

    def get_args(self):
        return self.args

    def get_err_msg(self):
        return self.err_msg
