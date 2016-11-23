#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

import  threading
import util.AndroidUtil
import util.AdbUtil
"""
function: 用于采集cpu数据的逻辑
date:2016/11/23

"""

class GetCpuDataThread(threading.Thread):
    times=30 #收集数据条数为30次
#     cycletime=60*60*4 #测试持续时长为4H
    cycletime=5*60 #测试持续时长为5min
    interval=cycletime/times#收集1次所需要的时间，单位为s
    CPUdata=[]#用于收集所有的CPU数据
    CPUerror=[]#用于手机CPU占用过高的数据。
 
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.threadId = thread_id

    """
        获取cpu数据的逻辑
    """
    def run(self):
        while i<times:
            cpudata=AndroidUtil.get_cpu_data()#当前采集到的数据
            if cpudata>=50.00:
                cpuerror=cpudata
                CPUerror.append(cpuerror)
                AdbUtil.screenshot()
            else:
                pass
            CPUdata.append(cpudata)
            i+=1
        return CPUerror,CPUdata
        pass
    
    
    
    