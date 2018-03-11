#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-09 18:27
from app.parseargs import parse
import os
import logging
import sys


def check_argument(err_msg):
    """
    检测用户输入的参数
    :return:
    """
    if err_msg:
        print('Oops 你输入的参数有错误，请根据以下信息做修改')
        print('\n'.join(err_msg))
        exit(1)


def logging_config(logfile, level):
    """
    配置日志
    :param logfile:
    :return:
    """
    loglevel = {1: logging.DEBUG, 2: logging.INFO, 3: logging.WARNING, 4: logging.ERROR, 5: logging.CRITICAL}
    abspath = os.path.abspath(logfile)
    pardir = abspath.rsplit(os.sep, 1)[0]
    if not os.path.exists(pardir):
        os.makedirs(pardir, exist_ok=True)
    logging.basicConfig(filename=abspath, level=loglevel.get(level, logging.INFO), filemode='w',
                        format='%(asctime)s %(levelname)s %(threadName)s "%(module)s.%(filename)s:%(funcName)s:%(lineno)d":%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('config logging finished.')
    logging.getLogger().setLevel(loglevel.get(level, logging.INFO))


parser = parse.ParseArgs()
args = parser.get_args()
check_argument(parser.get_err_msg())
logging_config(args.logfile, args.loglevel)
logging.debug('Argument input: {}'.format(sys.argv[1:]))
logging.debug('url={} logfile={} loglevel={} testself={} thread={} dbfile={} keyword={} depth={}'.format(args.url, args.logfile, args.loglevel, args.testself, args.thread, args.dbfile, args.keyword, args.depth))

