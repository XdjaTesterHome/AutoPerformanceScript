#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
"""
    用于存放fps数据
"""


class FpsData(models.Model):
    # 当前页面
    currentPage = models.TextField()
    # 测试页面的帧率
    fps = models.BigIntegerField()
    # 测试页面丢帧数目
    jankCount = models.BigIntegerField()
    # 测试应用的包名
    packageName = models.TextField()
    # 版本号
    versionCode = models.TextField()

    def __unicode__(self):
        return self.currentPage + '--' + self.packageName

    """
        批量的保存数据
    """
    def save_db_data(self, fps_data_dict, package_name):

        fps_list_to_insert = []
        fps_keys = fps_data_dict.keys()
        if len(fps_keys) <= 0:
            return
        for key in fps_keys:
            value = fps_data_dict.get(key)
            fps_list_to_insert.append(FpsData(currentPage=key, fps=value[0], jankCount=value[1], packageName=package_name, versionCode='0.0.0'))

        FpsData.objects.bulk_create(fps_list_to_insert)


