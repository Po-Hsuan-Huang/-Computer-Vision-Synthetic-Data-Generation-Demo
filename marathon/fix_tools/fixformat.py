#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 09:59:28 2017

@author: pohsuan

Fix the junk xml corrupted with worng xml format.

the junked .xml files are stored in junkxml.txt

junkxml.txt is created with test.py on server169 root dir.

"""

f = open('/home/pohsuan/disk1/Marathon/ImageSets/Main/5/junkxml.txt', 'r')
h = open('/home/pohsuan/disk1/Marathon/ImageSets/Main/5/junkxml2.txt', 'w')
word = ''
for i, text in enumerate(list(f.readline())):
    i=i+1
    if i%7 != 0:
        word+=str(text)
    elif i%7 == 0:
        word+=str(text)
        h.write(word + '\n')
        word= ''
        
f.close()