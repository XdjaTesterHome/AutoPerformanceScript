#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lzz'

from controller import GetCpuDataThread
from controller import GetMemoryThread
runMemory = GetMemoryThread.GetMemoryThread(1)
runCpu = GetCpuDataThread.GetCpuDataThread(1)
runMemory.start()
runCpu.start()
