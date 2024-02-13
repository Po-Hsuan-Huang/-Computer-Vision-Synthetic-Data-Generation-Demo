#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:21:37 2017

@author: pohsuan
"""

'''


generate .txt files needed for faster-rcnn training and testing.

ImageSetss/Main/trainval.txt
ImageSet/Main/test.txt 

are two index files tracking which image to be used during training and testing.

Options :
    PlainGen : generate filenames according to designated 'start' and 'stop'
    XMLGen : generate filenames accroding to the .xml files in the respective folder
    JPGGen : generate filenames accroding to the .jpg files in the respective folder

-----------------------------------------------------------------
Note : 
 
    
'''

import glob, sys, os
'''Mode :'''
PlainGen = False
XMLGen = False
JPGGen = True
    
'''Parameters'''

folder = 3

start = 1
stop  = 100000
dest = 'test.txt'

#files = sorted(glob.glob('/home/pohsuan/Documents/Marathon2017/data/Annotations/TrainSet'+str(folder)+'/*.xml' ))
#files = sorted(glob.glob('/home/pohsuan/disk1/Marathon/testImages/*jpg' ))
#src_path ='/home/pohsuan/Documents/Marathon2017/tag_pics/realpho2016phone/'
src_path ='/home/pohsuan/Desktop/test/'

files = sorted(glob.glob( src_path + '*.jpg' ))

#%%

#data_path = '/home/pohsuan/Documents/Marathon2017/data/ImageSets/Main/'+ str(folder) + '/'
#dest_path = '/home/pohsuan/Documents/Marathon2017/tag_pics/realpho2016phone/'
dest_path = '/home/pohsuan/Desktop/test/'


if os.path.isdir(dest_path):
    if len(glob.glob(dest_path +"*.txt")) != 0 :
         anw = raw_input( ' Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
         if anw.lower() != "y":
             sys.exit()
else:
    os.makedirs(dest_path)

with open(dest_path + dest, 'w') as g:
    if PlainGen:
        for x in range(start, stop + 1 ):
             filename = '{:07d}'.format(x)
             g.write(filename + '\n')
             
    if XMLGen:
        for x in files:
            x = x.split('.xml')[0]
            x = x.split(src_path)[1]
#            x = x.split('/home/pohsuan/disk1/Marathon/testImages/')[1]
            x = int(x)
            filename = '{:08d}'.format(x)
            
            g.write(filename + '\n')
    if JPGGen:
        for x in files:
            x = os.path.splitext(os.path.basename(x))[0]
            x = int(x)
            filename = '{:07d}'.format(x)
            
            g.write(filename + '\n')
        