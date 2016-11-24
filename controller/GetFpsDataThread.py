#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import threading
import time
import common.GlobalConfig as config
from util.AndroidUtil import AndroidUtil
from util.AdbUtil import AdbUtil

__author__ = 'zhouliwei'

"""
function: 获取帧率的数据
date:2016/11/24

"""


class GetFpsDataThread(threading.Thread):

    # 存放采集到的帧率数据
    fps_datas = [['frame_count', 'jank_count', 'fps', 'page']]

    # 存放有问题的帧率数据
    fps_error_datas = [['frame_count', 'jank_count', 'fps', 'page', 'pic_name']]

    def __init__(self, package_name):
        threading.Thread.__init__(self)
        self.package_name = package_name

        # 每次采集数据前，先清理上次的数据
        GetFpsDataThread.clear_data()

    """
        采集数据的逻辑
    """
    def run(self):
        def handle_error_data(frame_count, jank_count, fps, current_page):
            # 暂时当fps < 50 或者 jank_count > 10 我们认为是不达标的
            if fps < 50 or jank_count > 10:
                # 截图
                timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
                pic_name = 'fps' + timestamp
                AdbUtil.screenshot(pic_name)
                # 保存日志

                GetFpsDataThread.fps_error_datas.append([frame_count, jank_count, fps, current_page, pic_name])

        # 死循环，满足条件后跳出
        exec_count = 0
        while True:
            # 判断执行了多少次
            if exec_count > config.collect_data_count:
                break

            # 采集数据
            frame_count, jank_count, fps = AndroidUtil.get_fps_data_by_gfxinfo(self.package_name)
            current_page = AndroidUtil.get_cur_activity()
            GetFpsDataThread.fps_datas.append([frame_count, jank_count, fps, current_page])

            # 处理有问题的数据
            handle_error_data(frame_count, jank_count, fps)
            exec_count += 1

            # 采集数据时间间隔
            time.sleep(config.collect_data_interval)
        print GetFpsDataThread.fps_datas

    """
        用于清理数据
    """
    @staticmethod
    def clear_data():
        GetFpsDataThread.fps_datas = [['frame_count', 'jank_count', 'fps', 'page']]
        GetFpsDataThread.fps_error_datas = [['frame_count', 'jank_count', 'fps', 'page', 'pic_name']]

if __name__ == '__main__':
    GetFpsDataThread('com.xdja.safekeyservice').start()