#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'lzz'

import  threading
import util.AndroidUtil
import util.AdbUtil
"""
function: 采集内存数据的逻辑
date:2016/11/23

"""


class GetMemoryDataThread(threading.Thread):
    
    times=30 #收集数据条数为30次
#     cycletime=60*60*4 #测试持续时长为4H
    cycletime=5*60 #测试持续时长为5min
    interval=cycletime/times#收集1次所需要的时间，单位为s
    Memorydata=[]#用于收集所有的内存数据
    Memoryerror=[]#用于手机内存占用过高的数据。
    
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.threadId = thread_id

    """
        采集内存数据的逻辑
    """
    def run(self):
        while i<times:
            memorydata=AndroidUtil.get_memory_data()#当前采集到的数据
            if memorydata>=50*1024:
                memoryerror=memorydata
                Memoryerror.append(memoryerror)
                AdbUtil.screenshot()
            else:
                pass
            Memorydata.append(memorydata)
            i+=1
        return Memoryerror,Memorydata
        pass