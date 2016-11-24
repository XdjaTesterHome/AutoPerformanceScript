#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

import common.GlobalConfig as config
"""
function: 用于打印日志
date:2016/11/23

"""


class LogUtil(object):

    """
        用于打印一般信息
    """
    @staticmethod
    def log_i(info):
        if config.log_switch:
            print info

    """
        用于打印错误信息
    """
    @staticmethod
    def log_e(error):
        if config.log_switch:
            print '[ERROR] : ' + error
