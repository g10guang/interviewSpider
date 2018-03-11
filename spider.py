#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-10 14:59
import time
from app import args
from app.spider import spider
from app.store import sqlitedb
import logging
from app.spider import testself


def startup():
    if args.testself:
        spiderman = testself.TestSelf()
    else:
        db = sqlitedb.SqliteStore(args.dbfile)
        spiderman = spider.Spider(args.url, args.keyword, args.depth, db)
    print('开始爬取 {} ......\n'.format(args.url))
    sleep_time = args.flush
    # 此后将 main-Thread 设置为每 10s 刷新控制台进度消息
    while not spiderman.has_finished():
        print(end='\r')
        finish, total = spiderman.progress()
        print('已完成：{} 已发现：{} 百分比：{}'.format(finish, total, finish / total), end='', flush=True)
        time.sleep(sleep_time)
    finish, total = spiderman.progress()
    print('\r已完成：{} 已发现：{} 百分比：{}'.format(finish, total, finish / total), end='', flush=True)
    print('\nfinish')
    logging.debug('spider exit')


if __name__ == '__main__':
    startup()
