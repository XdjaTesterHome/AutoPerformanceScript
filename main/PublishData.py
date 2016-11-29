#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

"""
function: 用于将收集的数据上报
date:2016/11/25

"""
class PublishData(object):

    """
        用于对收集的数据进行预处理
        预处理的规则：对同一类数据，筛选出同一页面的数据，做平均值。
    """
    def pre_process_data(self):
        pass

    """
        用于对处理后的数据发布
    """
    def publish_data(self):
        pass