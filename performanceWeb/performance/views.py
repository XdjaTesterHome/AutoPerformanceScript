#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here. 在这里添加各种界面

"""
    index界面
"""


def home(request):
    return render(request, 'home.html')
