#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-09 18:27
from app.parseargs import parse
import logging
import os

parser = parse.ParseArgs()
args = parser.get_args()


def logging_config(logfile, loglevel=logging.DEBUG):
    """
    配置日志
    :param logfile:
    :return:
    """
    abspath = os.path.abspath(logfile)
    pardir = abspath.rsplit(os.sep, 1)[0]
    if not os.path.exists(pardir):
        os.makedirs(pardir, exist_ok=True)
    logging.basicConfig(filename=abspath, level=logging.DEBUG, filemode='w',
                        format='%(asctime)s %(levelname)s %(threadName)s "%(module)s.%(filename)s.%(funcName)s:%(lineno)d":%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('config logging finished.')


logging_config(args.logfile)
