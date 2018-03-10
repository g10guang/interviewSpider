#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-03-10 10:33

import threading
from queue import Queue


class ThreadPool:
    """
    线程池
    """

    def __init__(self, workers: int, fn, queue_size: int=1000):
        # 任务队列
        self.workers = workers
        self.fn = fn
        self.task_queue = Queue(queue_size)
        self.pool = []
        self.__init_thread_pool()

    def __init_thread_pool(self):
        """
        初始化线程池
        :return:
        """
        self.pool.extend([Worker(self.task_queue, self.fn) for _ in range(self.workers)])

    def submit(self, task: tuple):
        """
        提交任务
        :return:
        """
        self.task_queue.put(task)

    def shutdown(self):
        """
        等待所有线程执行的任务完成
        :return:
        """
        for t in self.pool:
            t.stop()
        for t in self.pool:
            if t.is_alive():
                t.join()


class Worker(threading.Thread):
    """
    工作线程
    """

    def __init__(self, task_queue, fn):
        self.fn = fn
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.start()
        self.daemon = True
        self.run_flag = True

    def run(self):
        """
        重写 run 方法，执行相应的逻辑
        从任务队列中取出一个任务，然后执行任务
        :return:
        """
        while self.run_flag:
            task = self.task_queue.get()
            self.fn(task)

    def stop(self):
        """
        通知本线程退出
        :return:
        """
        self.run_flag = False
