#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

import  threading
"""
function: 用于采集cpu数据的逻辑
date:2016/11/23

"""


class GetCpuDataThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.threadId = thread_id

    """
        获取cpu数据的逻辑
    """
    def run(self):
        pass