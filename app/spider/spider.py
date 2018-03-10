#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-10 10:06
import threading

import requests
from requests_html import HTMLSession, HTMLResponse

from app import args
from app.threadpool import ThreadPool
from app.store import sqlitedb
import logging


class Spider:
    """
    网络爬虫
    当前仅支持爬取 HTML 网页，对于 XML / plaintext 尚未支持
    """

    def __init__(self, base_url, keyword, max_depth, db: sqlitedb.SqliteStore):
        self.url = base_url
        self.keyword = keyword
        self.max_depth = max_depth
        self.db = db
        self._session = HTMLSession()
        # 记录已经被访问过的 url 并且记录是在第几层访问
        # https://docs.python.org/3/glossary.html#term-global-interpreter-lock 描述 dict 是线程安全的
        self.analysed_url = dict()
        self.url_visiting = dict()
        self._mutex = threading.Lock()
        self.dblock = threading.Lock()
        self.url_with_keyword = dict()
        self._thread_pool = ThreadPool(args.thread, fn=self.analyse)
        self._thread_pool.submit((base_url, 0))
        logging.debug('start Spider base_url={} keyword={} max_depth={}'.format(self.url, self.keyword, self.keyword, self.max_depth))

    def analyse(self, task):
        """
        下载 HTML
        :param task: is a tuple (url, level)
        :return:
        """
        url, level = task
        if not self.check_url(url, level):
            logging.debug('get task {} which has been visited. Please check mutex use right or not'.format(task))
            return
        try:
            response = self._session.get(url)
            logging.debug('GET {}'.format(url))
        except requests.exceptions.ConnectionError as e:
            # 该 url 无法连接
            logging.warning('requests.exceptions.ConnectionError to {}'.format(url))
        except requests.exceptions.InvalidSchema as e:
            # 不支持该协议
            logging.critical('requests.exceptions.InvalidSchema an invalid Schema {}'.format(url))
        else:
            content_type = self.content_type(response)
            logging.debug('{} GET Content-Type={}'.format(url, content_type))
            # 目前仅仅支持 html
            if '/html' in content_type:
                has_key = self.has_keyword(response)
                if has_key:
                    try:
                        self._mutex.acquire()
                        self.url_with_keyword[url] = level
                        logging.info('url {} with keyword={}'.format(url, self.keyword))
                    except Exception as e:
                        logging.error(e)
                    finally:
                        self._mutex.release()
                links = self.extract_link(response)
                self.submit_links2queue(links, level + 1)
            else:
                logging.warning('url {} Content-Type={} not supported'.format(url, content_type))
        finally:
            self.add_url2analysed(url, level)

    def check_url(self, url, level):
        """
        检查 url 是否已经被爬取过，或者 url 是否正在被爬取
        :param level:
        :param url:
        :return:
        """
        flag = False
        try:
            self._mutex.acquire()
            # 这里检查顺序不能颠倒，否则有可能重复爬取同一个网页
            if url not in self.url_visiting and url not in self.analysed_url:
                self.url_visiting[url] = level
                flag = True
        except Exception:
            # TODO 日志报告错误
            pass
        finally:
            self._mutex.release()
        return flag

    def add_url2analysed(self, url, level):
        """
        将 url 加入到已经分析的 url 字典中
        :param url:
        :return:
        """
        try:
            self._mutex.acquire()
            # 先加到 analysed_url 再从 url_visiting 删除，防止重复爬取
            self.analysed_url[url] = level
            del self.url_visiting[url]
        except Exception as e:
            logging.error(e)
        finally:
            self._mutex.release()
            logging.info('finish url {} in level {}'.format(url, level))

    def extract_link(self, r: HTMLResponse):
        """
        提取 html 中的链接，需要分析相对链接和绝对链接
        :return:
        """
        relative_links = r.html.links - r.html.absolute_links
        all_links = r.html.absolute_links | self.relative2absolute(relative_links, r.html.base_url)
        logging.info('links {} in url {}'.format(all_links, r.url))
        return all_links

    def relative2absolute(self, relative_links, base_url):
        """
        将相对链接拼接成绝对链接
        :param relative_links:
        :param base_url:
        :return:
        """
        return {base_url + x for x in relative_links}

    def has_keyword(self, r: HTMLResponse) -> bool:
        """
        判断是否包含关键字
        只是使用简单的判断字符串是否存在与 text 中
        :param r:
        :return:
        """
        raw_text = self.extract_raw_text(r)
        if self.keyword in raw_text:
            logging.debug('keyword={} in url {}'.format(self.keyword, r.url))
            return True
        else:
            logging.debug('keyword={} not in url {}'.format(self.keyword, r.url))

    def extract_raw_text(self, r: HTMLResponse) -> str:
        """
        去除 HTML 标签，只留下看到的字符串
        作为优化可以检查 css 把隐藏标签等过滤掉
        :param r:
        :return:
        """
        text = ''
        try:
            # 这里的 text 已经把 title 给包含了
            text = r.html.text
        except Exception as e:
            logging.error(e)
        return text

    def submit_links2queue(self, links, level):
        """
        向队列中添加新任务
        :param links: 本次爬取页面中的所有链接
        :param level: 本次页面所处深度
        :return:
        """
        if level > self.max_depth:
            logging.debug('links {} beyond max_depth={}'.format(links, level))
            return
        for link in links:
            if link.startswith(self.url):   # 只搜索同一个域下的内容
                if link not in self.url_visiting and link not in self.analysed_url:
                    # 提交到队列中
                    self._thread_pool.submit((link, level))

    def has_finished(self):
        """
        查询当前爬虫任务是否已经完成
        :return:
        """
        f = self._thread_pool.has_finish()
        if f:
            self.persist2db()
        return f

    def persist2db(self):
        """
        将 url 持久化到 sqlite db
        :return:
        """
        try:
            self.dblock.acquire()
            t = self.url_with_keyword
            self.url_with_keyword = dict()
        finally:
            self.dblock.release()
        urls = [(self.keyword, url) for url in t]
        self.db.batch_insert(urls)

    def content_type(self, r: HTMLResponse) -> str:
        """
        获取一个相应头中的 Content-Type
        :param r:
        :return:
        """
        return r.headers.get('Content-Type', '')
