#!/usr/bin/env python      
# -*- coding: utf-8 -*-
from CollectData import CollectData
import common.GlobalConfig as config
from monkey.Monkey import Monkey

__author__ = 'zhouliwei'

"""
function: 脚本的主入口
date:2016/11/25

"""

run_monkey_count = 1000

"""
    程序的主入口
"""


def main_entrance():
    # 1. 判断是否满足采集数据的条件
    can_collect, tip_message = CollectData.can_collect_data(config.test_package_name)
    if not can_collect:
        print tip_message
        return
    # 2. 开启monkey
    Monkey().run_monkey(run_monkey_count, config.test_package_name)
    # 2. 开始采集数据的逻辑
    CollectData().auto_collect_data()

    # 3. 数据采集完成后,对采集到的数据处理并上报
    print CollectData.flow_error_datas
    print CollectData.flow_datas
    print CollectData.fps_datas
    print CollectData.fps_error_datas
    print 'performance data collect success'

main_entrance()