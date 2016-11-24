#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'lzz'
import  threading
import time
from util.AndroidUtil import AndroidUtil
from util.AdbUtil import AdbUtil
"""
function: 用于采集cpu数据的逻辑
date:2016/11/23

"""
AdbUtil = AdbUtil()
AndroidUtil = AndroidUtil()
class GetCpuDataThread(threading.Thread):
    times=30 #收集数据条数为30次
#     cycletime=60*60*4 #测试持续时长为4H
    cycletime=5*60 #测试持续时长为5min
    interval = cycletime/times#收集1次所需要的时间，单位为s
    CPUdata=[]#用于收集所有的CPU数据
    CPUerror=[]#用于手机CPU占用过高的数据。
 
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.threadId = thread_id

    """
        获取cpu数据的逻辑
    """
    def run(self):
        i = 0
        while i < self.times:
            cpudata = AndroidUtil.get_cpu_data()#当前采集到的数据
            if cpudata >= 50.00:
                cpuerror = cpudata
                self.CPUerror.append(cpuerror)
                AdbUtil.screenshot()
            else:
                pass
            self.CPUdata.append(cpudata)
            time.sleep(self.interval)#设定多久采集一次数据
            i += 1
        return self.CPUerror, self.CPUdata
        pass
    
if __name__ == '__main__':
    res = GetCpuDataThread(1)
    res.start()
    res.join()#子线程执行完毕，才能执行主线程
    print res.CPUdata, res.CPUerror  #这个就是主线程


    
    