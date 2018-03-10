#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-10 14:59
import time
from app import args
from app.spider import spider
from app.store import sqlitedb


def startup():
    db = sqlitedb.SqliteStore(args.dbfile)
    spiderman = spider.Spider(args.url, args.keyword, args.depth, db)
    sleep_time = 10
    # 此后将 main-Thread 设置为每 10s 刷新控制台进度消息
    while not spiderman.has_finished():
        time.sleep(sleep_time)


if __name__ == '__main__':
    startup()
