#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

from AdbUtil import AdbUtil
from LogUtil import LogUtil as log

import time
import re
import subprocess

"""
function: 用于操作Android相关的方法类
date:2016/11/22

"""


class AndroidUtil(object):
    def __init__(self):
        pass

    """
        获取cpu数据
    """

    def get_cpu_data(self):
        pass

    """
        获取内存数据
    """

    def get_memory_data(self):
        pass

    """
        获取帧率数据
        通过 adb shell dumpsys gfxinfo pkgName获取数据
        @:return (frame_count 帧数, jank_count 丢帧数, fps 帧率)
    """

    @staticmethod
    def get_fps_data_by_gfxinfo(pkg_name):

        # 为了验证一帧是否合格
        def validator(x):
            if x is None:
                return False

            xs = x.split('\t')
            # 必须要有三个数值
            if len(xs) < 2 or len(xs) > 5:
                return False

            return True

        # 为了处理通过adb shell dumpsys gfxinfo package_name 获得的结果
        def handle_fps_result(x):
            # 截取 【Profile data in ms:】之后的数据
            first_result = re.findall(r'Profile.*hierarchy', x, re.DOTALL)
            activity_name = re.findall(r'(com.*)/.*@', first_result[0])
            data = re.findall(r'Execute(.*?)\r\n\r\n', first_result[0], re.DOTALL)
            if len(data) > 1:
                result = data[1].strip().split('\r\n\t')
            else:
                result = data[0].strip().split('\r\n\t')

            return result

        try:
            cmd = 'dumpsys gfxinfo %s' % pkg_name
            fps_result = AdbUtil.exec_adb_shell(cmd)
            fps_result = handle_fps_result(fps_result)
            # 得到的fps_result中是包含\t的。
            frames = [frame for frame in fps_result if validator(frame)]

            frame_count = len(frames)
            jank_count = 0
            vsync_count = 0
            if len(frames) > 0:

                for frame in frames:
                    time_block = frame.strip().split('\t')

                    # 计算一帧渲染的时间
                    render_time = 0
                    try:
                        for i in range(len(time_block)):
                            render_time += float(time_block[i])
                            i += 1
                    except Exception as e:
                        log.log_e('render_time get failure' + e.message)

                    """
                    执行一次命令，总共收集到了m帧（理想情况下m=128），但是这m帧里面有些帧渲染超过了16.67毫秒，算一次jank，一旦jank，
                    需要用掉额外的垂直同步脉冲。其他的就算没有超过16.67，也按一个脉冲时间来算（理想情况下，一个脉冲就可以渲染完一帧）

                    所以FPS的算法可以变为：
                    m / （m + 额外的垂直同步脉冲） * 60
                    """
                    if render_time > 16.67:
                        jank_count += 1
                        if render_time % 16.67 == 0:
                            vsync_count += int(render_time / 16.67) - 1
                        else:
                            vsync_count += int(render_time / 16.67)
                fps = int(frame_count * 60) / (frame_count + vsync_count)

                return frame_count, jank_count, fps
            else:
                # 不滑动，没有帧率数据时返回0,0,0
                return 0, 0, 0
        except Exception as e:
            log.log_e('get fps failure,please check ' + e.message)

    """
        获取kpi数据
        从一个页面跳转到另一个页面的时间
    """

    def get_kpi_data(self, package_name):
        cmd = 'adb logcat -c && adb logcat -v time -s ActivityManager | findStr %s' % package_name
        results = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        while True:
            data = results.stdout.readline()
            print data
            if data == b'':
                if results.poll() is not None:
                    break
            else:
                pass

        pass

    """
        获取电量数据
    """

    def get_battery_data(self):
        pass

    """
        获取对应包名的流量消耗情况
        基于UID获取App的网络流量的方法
        注意：这里得到的流量是从开启App之后累积的，计算一段时间内的流量需要前后两次流量做差
        从/proc/net/xt_qtaquid/stats  获取网络流量统计，进行判断，不存在使用之前的cat /proc/uid_stat/{1}/tcp_snd方法获取
        @:return 第六列为rx_bytes   接收数据
                 第八列为tx_bytes   传输数据
    """

    @staticmethod
    def get_flow_data(package_name):
        uid = AdbUtil.get_uid(package_name)
        if uid == 0:
            log.log_i('app uid is 0, check app 是否打开')
            return 0, 0
        cmd = 'cat /proc/net/xt_qtaguid/stats'
        flag_net = AdbUtil.exec_adb_shell(cmd)
        if 'No such file or directory' not in flag_net:
            try:
                cmd = 'cat /proc/net/xt_qtaguid/stats | grep %s' % uid
                str_uid_net_stats = AdbUtil.exec_adb_shell(cmd)
                # 有可能有多行数据
                list_rx = []  # 接收网络数据流量列表
                list_tx = []  # 发送网络数据流量列表
                for item in str_uid_net_stats.splitlines():
                    rx_bytes = item.split()[5]
                    tx_bytes = item.split()[7]
                    list_rx.append(int(rx_bytes))
                    list_tx.append(int(tx_bytes))
                float_total_net_traffic = (sum(list_rx) + sum(list_tx)) / 1024.0 / 1024.0
                float_total_net_traffic = round(float_total_net_traffic, 4)
                return sum(list_rx), sum(list_tx), float_total_net_traffic
            except Exception, e:
                log.log_e('cannot get flow from /proc/net/xt_qtaguid/stats' + e)
        else:
            try:
                cmd_snd = 'cat /proc/uid_stat/%s/tcp_snd' % uid
                cmd_rec = 'cat /proc/uid_stat/%s/tcp_rcv' % uid
                str_totalTxBytes = AdbUtil.exec_adb_shell(cmd_snd)
                str_totalRxBytes = AdbUtil.exec_adb_shell(cmd_rec)
                if 'No such file or directory' not in str_totalTxBytes and 'No such file or directory' not in str_totalRxBytes:
                    float_total_net_traffic = (int(str_totalRxBytes) + int(str_totalTxBytes)) / 1024.0 / 1024.0
                    float_total_net_traffic = round(float_total_net_traffic, 4)
                    return int(str_totalRxBytes), int(str_totalTxBytes), float_total_net_traffic
            except Exception as e:
                log.log_e('cannot get flow from /proc/uid_stat/tcp_snd  or tcp_rcv' + e)

        return 0, 0, 0


if __name__ == '__main__':

    for i in range(20):
        time.sleep(1)
        print AndroidUtil.get_fps_data_by_gfxinfo('com.tencent.mm')
        i += 1
