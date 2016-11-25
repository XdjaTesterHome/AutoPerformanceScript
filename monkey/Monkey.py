#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lzz'
from util import AdbUtil
mokeyrun = AdbUtil.AdbUtil()
class Monkey():
    def __init__(self):
        pass
#runmonkey,time为测试monkey时长，pkg为测试包#
    def runmonkey(self,time,pkg):
        cmd_Memory = "adb shell monkey -p "+ pkg +" --throttle 500 --ignore-crashes --ignore-timeouts --ignore-native-crashes -v -v -v %s"%(time)
        mokeyrun.exadb(cmd_Memory)
        pass
if __name__== "__main__":
    Monkey().runmonkey(100,"com.xdja.safekeyservice")