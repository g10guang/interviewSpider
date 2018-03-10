#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-09 23:55
import sys


def mock_sys_argv():
    """
    模拟命令行输入，向 sys.argv 中添加参数
    :return:
    """
    mock_args = ['-u', 'http://g10guang.com', '-f', './log.txt', '-l', '1', '-thread', '3', '-dbfile', './spider.db', '--key="hello"']
    sys.argv.extend(mock_args)