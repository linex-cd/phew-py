#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config
@author: chineseocr
"""
ocrType = 'chinese'
ocrPath  = 'ocrcore/models/ocr/{}/ocr.weights'.format(ocrType)
textPath = 'ocrcore/models/text/text.weights'
darkRoot ='/home/darknet/libdarknet.so' ##darknet 
TEXT_LINE_SCORE=0.5##text line prob
scale = 600 #900 ##可动态修改 no care text.cfg height,width
maxScale = 900 #1800
GPU=True ## gpu for darknet  or cpu for opencv.dnn 
anchors = '16,11, 16,16, 16,23, 16,33, 16,48, 16,68, 16,97, 16,139, 16,198, 16,283'
