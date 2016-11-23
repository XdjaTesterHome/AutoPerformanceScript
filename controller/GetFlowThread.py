#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

import threading
"""
function: 用于获取流量的线程
date:2016/11/23

"""


class GetFlowThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.threadID = thread_id

    """
        采集数据的逻辑写在这里
    """
    def run(self):
        pass