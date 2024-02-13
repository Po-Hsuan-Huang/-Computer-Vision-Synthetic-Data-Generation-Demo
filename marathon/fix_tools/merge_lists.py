#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:34:51 2017

@author: pohsuan


merge two txt files if the file is preseted in both lists.
"""
f1 = open('/home/pohsuan/disk1/Marathon/ImageSets/Main/5/mergedtrainval.txt', 'r')
f3 = open('/home/pohsuan/disk1/Marathon/ImageSets/Main/5/mergedtrainval3.txt', 'r')
f4 = open('/home/pohsuan/disk1/Marathon/ImageSets/Main/5/junkxml2.txt', 'r')
f5 = open('/home/pohsuan/disk1/Marathon/ImageSets/Main/5/trainval.txt', 'r')
#f6 = open('/home/pohsuan/disk1/Marathon/ImageSets/Main/5/trainval_predator.txt', 'r')
#f7 = open('/home/pohsuan/disk1/Marathon/ImageSets/Main/5/trainvalNitroFo.txt', 'r')

F1= sorted(list(f1))
F3, F4, F5= sorted(list(f3)), sorted(list(f4)), sorted(list(f5))
U = F1
for i, ff in enumerate([F1,F3,F4,F5]):
    U =set(U).intersection(ff)
dst = open('/home/pohsuan/disk1/Marathon/ImageSets/Main/5/mergedtrainvalFinal.txt', 'w')

for it in U:
#    filename = '{:07d}'.format(it)
#    dst.write(filename + '\n')
    dst.write(it)
    
dst.close()
f1.close()
f3.close()
f4.close()
f5.close()

