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
function: 用于收集数据并进行处理的逻辑
date:2016/11/25

"""


class CollectData(object):
    # 线程id
    MEMORY_THREAD_ID = 101
    CPU_THREAD_ID = 102
    KPI_THREAD_ID = 103
    FLOW_THREAD_ID = 104
    FPS_THREAD_ID = 105

    # 用于存放计算之后的值[平均fps, 平均jank_count]
    fps_data_dict = {}

    def __init__(self):
        pass

    """
        用于开始自动收集数据
    """

    def auto_collect_data(self):
        try:
            # # 这里同时启动多个线程，会有问题，后面解决
            # # 1. 开始采集kpi数据
            # kpi_thread = GetKpiDataThread(self.KPI_THREAD_ID, config.test_package_name)
            # kpi_thread.start()
            #
            # # 2. 开始采集内存数据
            # memory_thread = GetMemoryDataThread(self.MEMORY_THREAD_ID)
            # memory_thread.start()
            # # 3. 开始采集cpu数据
            # cpu_thread = GetCpuDataThread(self.CPU_THREAD_ID)
            # cpu_thread.start()

            # 4. 开始采集帧率数据
            fps_thread = GetFpsDataThread(self.FPS_THREAD_ID, config.test_package_name)
            fps_thread.start()
            fps_thread.join()
            #
            # # 5. 开始采集流量数据
            # flow_thread = GetFlowDataThread(self.FLOW_THREAD_ID, config.test_package_name)
            # flow_thread.start()

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
        return flow_task and fps_task and kpi_task and cpu_task and memory_task

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

    """
          用于对收集的数据进行预处理
          预处理的规则：对同一类数据，筛选出同一页面的数据，做平均值。
      """

    def pre_process_data(self):

        # 处理fps数据
        CollectData.__pre_fps_data(GetFpsDataThread.fps_datas)

    """
        用于对收集的fps数据进行处理
        fps采集到的数据格式是：[frame_count, jank_count, fps, current_page]
        处理数据的逻辑：通过current_page来求每个页面的fps平均值
                     通过一个map去存放，key是page_name,value是[fps_data, jank_count]
    """

    @staticmethod
    def __pre_fps_data(fps_datas):
        if len(fps_datas) <= 0:
            return

        for data in fps_datas:
            if len(data) <= 0:
                continue
            now_page_name = data[len(data) - 1]
            # 这里加个逻辑，假如fps和jank_count是0，就不进行计算
            if CollectData.fps_data_dict.has_key(now_page_name):
                if int(data[2]) == 0 and int(data[1]) == 0:
                    continue
                last_fps_datas = CollectData.fps_data_dict.get(now_page_name)
                now_fps_data = (int(data[2]) + int(last_fps_datas[0])) / 2
                now_jank_count = (int(data[1]) + int(last_fps_datas[1])) / 2
            else:
                if int(data[2]) == 0 and int(data[1]) == 0:
                    continue
                # 不包含当前页面，就直接添加
                now_fps_data = int(data[2])
                now_jank_count = int(data[1])

            CollectData.fps_data_dict[now_page_name] = [now_fps_data, now_jank_count]