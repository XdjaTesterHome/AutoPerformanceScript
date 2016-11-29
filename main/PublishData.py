#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import os, sys
import django
BaseDir = os.path.dirname(os.path.abspath(os.getcwd()))
sys.path.append(BaseDir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "performanceWeb.performanceWeb.settings")
django.setup()

from CollectData import CollectData
from performanceWeb.performance.models import FpsData
import common.GlobalConfig as config
__author__ = 'zhouliwei'

"""
function: 用于将收集的数据上报
date:2016/11/25

"""


class PublishData(object):

    def __init__(self):
        pass

    """
        用于对处理后的数据发布
    """

    @staticmethod
    def publish_data():
        PublishData.publish_fps_data(CollectData.fps_data_dict, config.test_package_name)
        pass

    """
        将fps数据写入到数据库
    """
    @staticmethod
    def publish_fps_data(fps_data_dict, package_name):
        FpsData().save_db_data(fps_data_dict, package_name)