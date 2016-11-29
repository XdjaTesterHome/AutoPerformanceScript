#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here. 在这里添加各种界面

"""
    index界面
"""


def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'base.html')
