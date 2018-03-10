#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-09 23:44

import unittest
from app.parseargs import parse
from app.utils import sysargs
import re


class TestParseArgs(unittest.TestCase):

    def setUp(self):
        sysargs.mock_sys_argv()
        parser = parse.ParseArgs()
        self.args = parser.get_args()

    def test_url(self):
        print(self.args.url)

    def test_testself(self):
        print(self.args.testself)

    def test_logfile(self):
        print(self.args.logfile)

    def test_loglevel(self):
        print(self.args.loglevel)

    def test_dbfile(self):
        print(self.args.dbfile)

    def test_keyword(self):
        print(self.args.key)

