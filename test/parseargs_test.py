#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-09 23:44

import unittest

from app.parseargs import parse
from app.utils import sysargs


class TestParseArgs(unittest.TestCase):

    def setUp(self):
        sysargs.mock_sys_argv()
        parser = parse.ParseArgs()
        self.args = parser.get_args()

    def test_url(self):
        assert self.args.url == 'http://g10guang.com'

    def test_testself(self):
        assert self.args.logfile == './log.txt'

    def test_logfile(self):
        assert self.args.loglevel == 1

    def test_loglevel(self):
        assert self.args.thread == 3

    def test_dbfile(self):
        assert self.args.dbfile == './spider.db'

    def test_keyword(self):
        # print(self.args.keyword)
        assert self.args.keyword == '"hello"'

