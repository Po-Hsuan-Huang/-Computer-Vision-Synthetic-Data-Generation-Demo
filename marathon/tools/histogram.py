#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 09:14:38 2017

@author: acer

This file check the distribution of categories of data by ploting a bargraph.
"""
import glob
import matplotlib.pylab as plt
import xml.etree.ElementTree as ET
import numpy as np
import fnmatch
import os
xml_list = sorted(glob.glob('/home/pohsuan/Documents/Marathon2017/data/Annotations/TrainSet2/*.xml'))

xml_list = []
src = '/home/pohsuan/Documents/Marathon2017/data/Annotations/TrainSet3/'

for root, dirnames, filenames in os.walk(src):
    for filename in fnmatch.filter(filenames, '*.xml'):
        xml_list.append(os.path.join(root, filename))
        
categories = {"tag": 0, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, 
              "J": 10, "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, 
              "S": 19, "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26, "0":27, 
              "1": 28 ,"2":29,"3":30,"4":31,"5":32,"6":33,"7":34,"8":35,"9":36}

hist= np.zeros(37)
n = 0
for n, filename in enumerate(xml_list): 
    src = open(filename, 'r')
    if n >10000:break

    try:
        tree = ET.parse(src)
        objs = tree.findall('object')
        for ix, obj in enumerate(objs):
            cat = obj.find('name')
            index = categories[cat.text]
            hist[index] += 1
    except:
        print filename
        pass

            
left_mark = np.arange(1,37,1)    
TL = np.asarray(['tag']+(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')))

plt.bar(left_mark, hist[1:], tick_label=TL[1:])
        