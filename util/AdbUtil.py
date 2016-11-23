#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

import os
import subprocess
"""
function: 处理和adb命令相关的工具类
date:2016/11/23

"""


class AdbUtil(object):
    def __init__(self):
        pass

    """
        执行adb命令
    """

    @staticmethod
    def exec_adb(commands):
        command_result = ''
        cmd = 'adb shell %s' % commands
        results = os.popen(cmd, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        results.close()
        return command_result

    """
    执行adb shell命令
    """

    @staticmethod
    def exec_adb_shell(command):
        command_result = ''
        cmd = 'adb shell %s' % command
        results = os.popen(cmd, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        results.close()
        return command_result

    """
        检查设备是否连接
    """

    @staticmethod
    def attach_devices():
        result = AdbUtil.exec_adb("devices")
        devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
        flag = [device for device in devices if len(device) > 2]
        if flag:
            return True
        else:
            return False

    """
       卸载apk
    """
    @staticmethod
    def uninstall_apk(package_name):
        result = AdbUtil.exec_adb("uninstall %s" % package_name)
        if 'Faliure' in result:
            return False
        else:
            return True

    """
       安装apk
    """
    @staticmethod
    def install_apk(apk_path):
        result = AdbUtil.exec_adb('install -rf %s' % apk_path)
        if 'Success' in result:
            return True
        else:
            return False

    """
        获取应用的pid
    """
    @staticmethod
    def get_pid(package_name):
        try:
            cmd = "ps | grep %s  | awk '{print $2}'" % package_name
            result = AdbUtil.exec_adb_shell(cmd)
            result = result.strip()

        except Exception, e:
            print e
            result = 0
        return result

    """
        获取app的uid
    """
    @staticmethod
    def get_uid(package_name):
        try:
            pid = AdbUtil.get_pid(package_name)
            pid = pid.split('\n')[0]

            cmd = 'cat /proc/'+ str(pid) + '/status | grep Uid'
            result = AdbUtil.exec_adb_shell(cmd)
            result = result.split('\t')[1]

        except Exception, e:
            print e
            result = 0
        return result


if __name__ == '__main__':
    print  AdbUtil.get_uid('com.tencent.mm')