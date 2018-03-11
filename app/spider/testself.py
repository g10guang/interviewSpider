#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-11 17:22
from app.spider import spider
from app.store import sqlitedb


class TestSelf(spider.Spider):
    """
    程序自测
    """

    def __init__(self, base_url: str = 'http://g10guang.com', keyword: str = 'Golang', max_depth: int = 3):
        print('程序自测')
        print('爬取 {} 上所有包含关键字 Golang 的页面'.format(base_url, keyword))
        db = sqlitedb.SqliteStore(dbfile='spider.db')
        super(TestSelf, self).__init__(base_url=base_url, keyword=keyword, max_depth=max_depth, db=db)
