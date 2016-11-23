#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'lzz'

import  threading
"""
function: 采集内存数据的逻辑
date:2016/11/23

"""


class GetMemoryDataThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.threadId = thread_id

    """
        采集内存数据的逻辑
    """
    def run(self):
        pass