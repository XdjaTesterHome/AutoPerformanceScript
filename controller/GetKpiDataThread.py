#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import threading
import time
import subprocess
import re
import common.GlobalConfig as config
from util.LogUtil import LogUtil as log

__author__ = 'zhouliwei'

"""
function: 获得kpi相关的数据。
          kpi数据想着是通过 adb logcat -c && adb logcat -v time -s ActivityManager | findStr pkgName获取
date:2016/11/24

"""


class GetKpiDataThread(threading.Thread):
    # 用于收集kpi的数据
    kpi_datas = [['now_page', 'jump_page', 'cost_time']]

    # 当前页面名称
    now_page_name = ''

    # 跳转页面名称
    jump_page = ''

    # 跳转花费时间
    cost_time = ''

    def __init__(self, thread_id, package_name):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.package_name = package_name

    """
        循环获取kpi数据的逻辑
    """

    def run(self):
        # 记录起始时间
        global results
        start_time = time.mktime(time.localtime())
        cmd = 'adb logcat -c && adb logcat -v time -s ActivityManager | findStr %s' % self.package_name
        try:
            results = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        except Exception as e:
            log.log_e('get kpi failure ' + e.message)

        # 这里的逻辑是采集一定时间的数据之后，结束进程
        while True:

            # 1. 根据时间判断是否结束
            now_time = time.mktime(time.localtime())
            if now_time - start_time > config.collect_data_time:
                if results.poll() is None:
                    print 'results.terminate()'
                    results.stdout.close()
                break
            # 2.读取内容，并分析
            data = results.stdout.readline()
            print data
            # 处理读取到的String
            if data is not None:
                if 'Displayed' in data:
                    # 1. 获取跳转页面的名称及时间，过滤 Displayed
                    result = data.split('Displayed')
                    result = result[1].strip().split(':')
                    if len(result) < 1:
                        self.jump_page = 'unknow'
                        self.cost_time = 0
                    else:
                        self.jump_page = result[0]
                        self.cost_time = result[1]

            # 2. 获取从哪个页面跳转
            if 'Moving to STOPPED:' in data:
                now_page = data.split('Moving to STOPPED:')
                now_page = now_page[1].strip().split(' ')
                if len(now_page) > 3:
                    self.now_page_name = now_page[2]
                else:
                    self.now_page_name = 'unknow'

            # 将结果保存到数组中
            if self.now_page_name is not None and self.jump_page is not None and self.cost_time is not None:
                GetKpiDataThread.kpi_datas.append([self.now_page_name, self.jump_page, self.cost_time])
        print GetKpiDataThread.kpi_datas

    """
        用于清理数据
    """
    @staticmethod
    def clear_data():
        GetKpiDataThread.kpi_datas = ['now_page', 'jump_page', 'cost_time']


if __name__ == '__main__':
    GetKpiDataThread(101, 'com.xdja.safekeyservice').start()
