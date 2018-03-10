#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-09 23:17
import argparse
import logging
import sys


class ParseArgs:
    """
    解析命令行参数
    """

    def __init__(self):
        self.args = None
        self._parse()

    def _parse(self):
        """
        解析参数
        :return:
        """
        parser = argparse.ArgumentParser(description='网络爬虫')
        parser.add_argument('-u', dest='url', default='http://skoo.me/', metavar='http://g10guang.com', type=str, help='输入爬取的网站的 url')
        parser.add_argument('-f', dest='logfile', default='./log.txt', metavar='log.txt', type=str,
                            help='日志输出文件')
        parser.add_argument('-l', dest='loglevel', default=1, metavar='[1,5]', type=int, help='日志等级')
        parser.add_argument('--testself', dest='testself', action='store_const', const=True, default=False, help='自测试')
        parser.add_argument('-thread', dest='thread', default=10, metavar='10', type=int, help='线程池大小')
        parser.add_argument('-dbfile', dest='dbfile', metavar='./spider.db', default='spider.db', type=str,
                            help='sqlite3 数据保存文件')
        parser.add_argument('--key', dest='keyword', default='Go', metavar='keyword', type=str, help='搜索关键字')
        parser.add_argument('-d', dest='depth', default=5, metavar='5', type=int, help='爬虫分析的深度')
        self.args = parser.parse_args()
        logging.debug('Argument input: {}'.format(sys.argv[1:]))
        logging.debug('url={} logfile={} loglevel={} testself={} thread={} dbfile={} keyword={} depth={}'.format(self.args.url, self.args.logfile, self.args.loglevel, self.args.testself, self.args.thread, self.args.dbfile, self.args.keyword, self.args.depth))
        self._validate()

    def _validate(self):
        """
        判断用户输入值是否合法
        :return:
        """
        # TODO

    def get_args(self):
        return self.args
