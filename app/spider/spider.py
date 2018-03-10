#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-10 10:06
import threading

from requests_html import HTMLSession, HTMLResponse

from app import args
from app.threadpool import ThreadPool


class Spider:
    """
    网络爬虫
    """

    def __int__(self, base_url, keyword):
        """

        :return:
        """
        self.url = base_url
        self.keyword = keyword
        self._thread_pool = ThreadPool(args.thread, fn=self.analyse)
        self._session = HTMLSession()
        # 记录已经被访问过的 url 并且记录是在第几层访问
        # https://docs.python.org/3/glossary.html#term-global-interpreter-lock 描述 dict 是线程安全的
        self.analysed_url = dict()
        self.url_visiting = dict()
        self._mutex = threading.Lock()
        self._thread_pool.submit((base_url, 0))
        self.url_with_keyword = dict()

    def analyse(self, task):
        """
        下载 HTML
        :param task: is a tuple (url, level)
        :return:
        """
        url, level = task
        if not self.check_url(url, level):
            return
        # TODO 这里链接有可能发生异常，需要处理
        response = self._session.get(url)
        has_key = self.has_keyword(response)
        if has_key:
            self.url_with_keyword[has_key] = level
        links = self.extract_link(response)
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
            # 这里检查顺序不能颠倒
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
            self._mutex.require()
            # 先加到 analysed_url 再从 url_visiting 删除，防止重复爬取
            self.analysed_url[url] = level
            del self.url_visiting[url]
        except Exception:
            # TODO 输出错误日志
            pass
        finally:
            self._mutex.release()

    def extract_link(self, r: HTMLResponse):
        """
        提取 html 中的链接，需要分析相对链接和绝对链接
        :return:
        """
        relative_links = r.html.links - r.html.absolute_links
        all_links = r.html.absolute_links | self.relative2absolute(relative_links, r.html.base_url)
        return all_links

    def relative2absolute(self, relative_links, base_url):
        """
        将相对链接拼接成绝对链接
        需要对 'mailto:g10guang@foxmail.com' 等链接做过滤处理
        :param relative_links:
        :param base_url:
        :return:
        """
        return {base_url + x for x in relative_links if not x.startswith('mailto:')}

    def has_keyword(self, r: HTMLResponse) -> bool:
        """
        判断是否包含关键字
        只是使用简单的判断字符串是否存在与 text 中
        :param r:
        :return:
        """
        raw_text = self.extract_raw_text(r)
        if self.keyword in raw_text:
            return True

    def extract_raw_text(self, r: HTMLResponse) -> str:
        """
        去除 HTML 标签，只留下看到的字符串
        作为优化可以检查 css 把隐藏标签等过滤掉
        :param r:
        :return:
        """
        text = r.html.text
        return text

    def submit_links2queue(self, links, level):
        """
        向队列中添加新任务
        :param links: 本次爬取页面中的所有链接
        :param level: 本次页面所处深度
        :return:
        """
        for link in links:
            if link not in self.url_visiting and link not in self.analysed_url:
                # 提交到队列中
                self._thread_pool.submit((link, level+1))
