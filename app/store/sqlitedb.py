#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-10 14:05
import sqlite3
import os
import logging


class SqliteStore:
    """
    将数据持久化到 sqlite3
    """

    def __init__(self, dbfile: str):
        self.dbfile = dbfile
        self.make_pardir()
        self.conn = sqlite3.connect(dbfile)
        self.c = self.conn.cursor()
        self.table_name = 'spider'
        self.create_table()
        print('数据将保存在 {} sqlite3 中'.format(self.table_name))

    def batch_insert(self, data: list):
        """
        将符合包含 keyword 的链接保存金数据库
        只要 links 中有一条数据不符合格式，就全部不执行插入操作
        :return:
        """
        if self.check_batch_data_format(data):
            self.c.executemany(
                '''INSERT INTO {table_name} (keyword, url) VALUES (?, ?)'''.format(table_name=self.table_name), data)
            self.persist()
            logging.info('batch insert {} into {} {} items'.format(data, self.table_name, len(data)))
        else:
            logging.error('batch insert {} into db file. Its format is invalid'.format(data))

    def single_insert(self, data: list):
        """
        插入单条数据
        如果数据格式不符合要求则不会执行插入操作
        :param data:
        :return:
        """
        if self.check_single_data_format(data):
            self.c.execute(
                '''INSERT INTO {table_name} (keyword, url) VALUES (?, ?)'''.format(table_name=self.table_name), *data)
            self.persist()
            logging.info('single insert {} into {}'.format(data, self.table_name))
        else:
            logging.error('single insert {} into db file. Its format is invalid'.format(data))

    def make_pardir(self):
        """
        创建文件夹
        :return:
        """
        abspath = os.path.abspath(self.dbfile)
        pardir = abspath.rsplit(os.sep, 1)[0]
        if not os.path.exists(pardir):
            logging.debug('{} not exists'.format(pardir))
            os.makedirs(pardir, exist_ok=True)
            logging.debug('make dir {}'.format(pardir))
        else:
            logging.debug('{} exists'.format(pardir))

    def create_table(self):
        """
        创建数据表
        :return:
        """
        result = self.c.execute('''SELECT name FROM sqlite_master WHERE name=? AND type="table"''', (self.table_name, ))
        if result.fetchall():
            logging.debug('table {} exists'.format(self.table_name))
        else:
            logging.debug('table {} not exists'.format(self.table_name))
            self.c.execute(
                '''CREATE TABLE IF NOT EXISTS {table_name} (id INT PRIMARY KEY, keyword TEXT, url TEXT)'''.format(table_name=self.table_name))
            logging.info('create table {}'.format(self.table_name))

    def check_batch_data_format(self, data) -> bool:
        """
        检查数据格式是否正确
        :return:
        """
        # 先检查一个对象是否可迭代的
        try:
            _ = iter(data)
        except TypeError:
            return False
        else:
            return all(len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], str) for item in data)

    def check_single_data_format(self, data) -> bool:
        """
        检查单条数据的格式
        :param data:
        :return:
        """
        return len(data) == 2 and isinstance(data[0], str) and isinstance(data[1], str)

    def persist(self):
        self.conn.commit()
        logging.debug('call conn.commit()')
