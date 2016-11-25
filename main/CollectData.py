#!/usr/bin/env python      
# -*- coding: utf-8 -*-
from util.LogUtil import LogUtil
from controller.GetFlowDataThread import GetFlowDataThread
from controller.GetKpiDataThread import GetKpiDataThread
from controller.GetFpsDataThread import GetFpsDataThread
from controller.GetCpuDataThread import GetCpuDataThread
from  controller.GetMemoryThread import GetMemoryDataThread

__author__ = 'zhouliwei'

"""
function: 用于收集数据的逻辑
date:2016/11/25

"""


class CollectData(object):
    # 线程id
    MEMORY_THREAD_ID = 101
    CPU_THREAD_ID = 102
    KPI_THREAD_ID = 103
    FLOW_THREAD_ID = 104
    FPS_THREAD_ID = 105

    def __init__(self):
        pass

    """
        用于开始自动收集数据
    """

    def auto_collect_data(self):
        try:
            # 1. 开始采集kpi数据
            kpi_thread = GetKpiDataThread(self.KPI_THREAD_ID, 'com.tencent')
            kpi_thread.start()

            # 2. 开始采集内存数据
            memory_thread = GetMemoryDataThread(self.MEMORY_THREAD_ID)
            memory_thread.start()

            # 3. 开始采集cpu数据
            cpu_thread = GetCpuDataThread(self.CPU_THREAD_ID)
            cpu_thread.start()

            # 4. 开始采集帧率数据
            fps_thread = GetFpsDataThread(self.FPS_THREAD_ID)
            fps_thread.start()

            # 5. 开始采集流量数据
            flow_thread = GetFlowDataThread(self.FLOW_THREAD_ID)
            flow_thread.start()

        except Exception as e:
            LogUtil.log_e('collect data failure ' + e.message)
