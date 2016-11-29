#!/usr/bin/env python      
# -*- coding: utf-8 -*-
from util.LogUtil import LogUtil
from controller.GetFlowDataThread import GetFlowDataThread
from controller.GetKpiDataThread import GetKpiDataThread
from controller.GetFpsDataThread import GetFpsDataThread
from controller.GetCpuDataThread import GetCpuDataThread
from controller.GetMemoryThread import GetMemoryDataThread
import common.GlobalConfig as config
from util.AdbUtil import AdbUtil
from util.AndroidUtil import AndroidUtil

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

    # 记录采集到的数据
    kpi_datas = []
    memory_datas = []
    cpu_datas = []
    fps_datas = []
    flow_datas = []

    # 记录采集到的异常数据
    kpi_error_datas = []
    memory_error_datas = []
    cpu_error_datas = []
    fps_error_datas = []
    flow_error_datas = []

    def __init__(self):
        pass

    """
        用于开始自动收集数据
    """

    def auto_collect_data(self):
        try:
            # 这里同时启动多个线程，会有问题，后面解决
            # 1. 开始采集kpi数据
            kpi_thread = GetKpiDataThread(self.KPI_THREAD_ID, config.test_package_name)
            kpi_thread.start()

            # 2. 开始采集内存数据
            memory_thread = GetMemoryDataThread(self.MEMORY_THREAD_ID)
            memory_thread.start()
            # 3. 开始采集cpu数据
            cpu_thread = GetCpuDataThread(self.CPU_THREAD_ID)
            cpu_thread.start()

            # 4. 开始采集帧率数据
            fps_thread = GetFpsDataThread(self.FPS_THREAD_ID, config.test_package_name)
            fps_thread.start()

            # 5. 开始采集流量数据
            flow_thread = GetFlowDataThread(self.FLOW_THREAD_ID, config.test_package_name)
            flow_thread.start()

            LogUtil.log_i('All thread worked!!')
        except Exception as e:
            LogUtil.log_e('collect data failure ' + e.message)

    """
        判断任务是否执行完成
    """
    @staticmethod
    def task_all_finish():
        flow_task = GetFlowDataThread.task_finish
        fps_task = GetFpsDataThread.task_finish
        kpi_task = GetKpiDataThread.task_finish
        cpu_task = GetCpuDataThread.task_finish
        memory_task = GetMemoryDataThread.task_finish
        if flow_task:
            print 'flow_task true'

        if fps_task:
            print 'fps_task true'

        if kpi_task:
            print 'kpi_task true'
        if cpu_task:
            print 'cpu_task true'
        if memory_task:
            print 'memory_task true'
        return flow_task and fps_task and kpi_task and cpu_task and memory_task
    """
        将采集到的数据记录下来
    """
    @staticmethod
    def record_data():
        CollectData.kpi_datas = GetKpiDataThread.kpi_datas
        CollectData.kpi_error_datas = GetKpiDataThread.kpi_error_datas
        GetKpiDataThread.clear_data()

        CollectData.cpu_datas = GetCpuDataThread.CPUdata
        CollectData.cpu_error_datas = GetCpuDataThread.CPUerror

        CollectData.memory_datas = GetMemoryDataThread.Memorydata
        CollectData.memory_error_datas = GetMemoryDataThread.Memoryerror

        CollectData.fps_datas = GetFpsDataThread.fps_datas
        CollectData.fps_error_datas = GetFpsDataThread.fps_error_datas
        GetFpsDataThread.clear_data()

        CollectData.flow_datas = GetFlowDataThread.flow_datas
        CollectData.flow_error_datas = GetFlowDataThread.flow_error_datas
        GetFlowDataThread.clear_data()

    """
        判断是否符合采集数据的条件
    """
    @staticmethod
    def can_collect_data(package_name):
        # 1. 判断手机是否连接
        mobile_connect = AdbUtil().attach_devices()
        tips = ''
        if not mobile_connect:
            tips = '请连接设备，当前无设备可用'
            return mobile_connect, tips

        # 2. 判断当前进程是否还活着
        process_alive = AndroidUtil.process_alive(package_name)
        if not process_alive:
            tips = 'app进程已被杀死，请打开app后再开始测试'
            return process_alive, tips

        return True, tips