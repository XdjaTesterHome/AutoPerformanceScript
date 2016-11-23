#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

"""
function: 用于操作Android相关的方法类
date:2016/11/22

"""
import os,time,re
import subprocess,re

class AndroidUtil(object):
    def __init__(self):
        pass

    """
        获取cpu数据  lzz，获取当前被监控的单个应用CPU的值
    """
    def get_cpu_data(self):
        #getCurrentPID:获取当前应用包名和Pid#
        def getCurrentPID(self):
            _result = os.popen('adb shell dumpsys activity top | findstr ACTIVITY').read().strip()
            _resultPid = re.findall(u'pid=(\d+)', _result)[0]
            _resultPName = re.findall(u'(com.\w+.\w+)',_result)[0]
            return [_resultPid,_resultPName]
        #getTotalCpuTime获取总jiffies数据#
        def getTotalCpuTime(self):
            _result = os.popen('adb shell cat /proc/stat').read().strip()
            _result = _result.split('\n')[0]
            _result = re.findall(u'(\d+)', _result)
            _result = reduce(lambda x,y:int(x) + int(y), _result)
            return _result
        #获取应用占用的总jiffies数据#pid:为应用进程pid
        def getPIDCpuTime(self,pid):
            _result = os.popen('adb shell cat /proc/%s/stat'%pid).read().strip()
            _result = re.findall(u'(\d+)', _result)
            _result = reduce(lambda x,y:x+y, [int(_result[11]),int(_result[12]),int(_result[13]),int(_result[14])]);
            return _result
        pid,pName = self.getCurrentPID()
        _start0 = self.getTotalCpuTime()
        _start1 = self.getPIDCpuTime(pid)
        time.sleep(1)
        _end0 = self.getTotalCpuTime()
        _end1 = self.getPIDCpuTime(pid)
        cpuUsage = float((_end1-_start1))/(_end0-_start0)*100#计算当前用户进程CPU的值
        CPU=(float('%.2f'%cpuUsage))#当前被监控应用CPU的值
        return CPU
        pass

    """
        获取内存数据lzz,获取被监控应用内存的值：Dalvik Heap alloc的值，单位为kb
    """
    def get_memory_data(self):
        #getCurrentPID:获取当前应用包名和Pid#
        def getCurrentPID(self):
            _result = os.popen('adb shell dumpsys activity top | findstr ACTIVITY').read().strip()
            _resultPid = re.findall(u'pid=(\d+)', _result)[0]
            _resultPName = re.findall(u'(com.\w+.\w+)',_result)[0]
            return [_resultPid,_resultPName]
        #readMemory采集应用Dalvik Heap alloc的值，单位为kb#
        def readMemory(pkgName):
            try:
                allocMemory = "0"
                cmd_Memory = "adb shell dumpsys meminfo " + pkgName
                cmdResult = subprocess.check_output(cmd_Memory,shell=True) 
                Result = re.search('.*(Dalvik Heap.*)',cmdResult,re.MULTILINE)
                if Result is not None:
                    res = Result.group()
                    res = res.split()
                    allocMemory = res[7]
            except Exception, e:
                print traceback.format_exc()
            finally:
                pass
            return allocMemory
        pid,pName = self.getCurrentPID()
        allocMemory=readMemory(pName)
        return allocMemory
        pass

    """
        获取帧率数据
    """
    def get_fps_data(self):
        pass

    """
        获取kpi数据
    """
    def get_kpi_data(self):
        pass

    """
        获取流量数据
    """
    def get_flow_data(self):
        pass

    """
        获取电量数据
    """
    def get_battery_data(self):
        pass
