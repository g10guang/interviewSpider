#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-10 10:33

import threading
from queue import Queue
import logging


class ThreadPool:
    """
    线程池
    """

    def __init__(self, worker_num: int, fn, queue_size: int = 10000):
        # 任务队列
        self.workers = worker_num
        self.fn = fn
        self.task_queue = Queue(queue_size)     # Queue 线程安全
        self.pool = []
        self.__init_thread_pool()
        self._task_num = 0
        self._task_finished = 0
        self._mutex = threading.Lock()

    def __init_thread_pool(self):
        """
        初始化线程池
        :return:
        """
        self.pool.extend([Worker(self.task_queue, self.fn, self.task_finish_callback) for _ in range(self.workers)])
        logging.debug('create ThreadPool size={}'.format(self.workers))

    def submit(self, task: tuple):
        """
        提交任务
        :return:
        """
        self._mutex.acquire()
        self._task_num += 1
        logging.debug('No.{} new task {}'.format(self._task_num, task))
        self._mutex.release()
        self.task_queue.put(task)

    def batch_submit(self, task_list: list):
        """
        批量提交任务，防止多次提交 submit，多次申请释放锁的耗时
        :return:
        """
        self._mutex.acquire()
        self._task_num += len(task_list)
        self._mutex.release()
        for task in task_list:
            self.task_queue.put(task)
            logging.debug('No.{} new task {}'.format(self._task_num, task))

    def shutdown(self):
        """
        等待所有线程执行的任务完成
        :return:
        """
        logging.debug('waiting worker thread to stop')
        for t in self.pool:
            t.stop()
        for t in self.pool:
            if t.is_alive():
                t.join()

    def has_finish(self):
        """
        判断任务是否已经完成
        :return:
        """
        f = self._task_num > 0 and self._task_num == self._task_finished
        if f:
            logging.debug('task queue has been finished.')
        return f

    def task_finish_callback(self):
        """
        线程每完成一个任务就回调该函数
        :return:
        """
        self._mutex.acquire()
        self._task_finished += 1
        logging.debug('finish No.{} task'.format(self._task_finished))
        self._mutex.release()

    def progress(self) -> tuple:
        """
        反馈进度消息，这里的进度消息不保证可靠
        :return:
        """
        return self._task_finished, self._task_num


class Worker(threading.Thread):
    """
    工作线程
    """

    def __init__(self, task_queue, fn, callback=None):
        self.fn = fn
        self.callback = callback
        threading.Thread.__init__(self)
        self.run_flag = True
        self.daemon = True
        self.task_queue = task_queue
        self.start()
        logging.debug('New worker {} create'.format(self.name))

    def run(self):
        """
        重写 run 方法，执行相应的逻辑
        从任务队列中取出一个任务，然后执行任务
        :return:
        """
        logging.debug('worker thread {} start main loop'.format(self.name))
        while self.run_flag:
            task = self.task_queue.get()
            logging.debug('worker thread {} get task {}'.format(self.name, task))
            self.fn(task)
            # 每完成一个任务执行回调
            if self.callback is not None:
                self.callback()
            logging.info('worker thread {} finish task {}'.format(self.name, task))
        logging.debug('worker thread {} exit main loop'.format(self.name))

    def stop(self):
        """
        通知本线程退出
        :return:
        """
        self.run_flag = False
        logging.info('worker thread run_flag={}', self.run_flag)
