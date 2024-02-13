#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:17:49 2017

@author: Po-Hsuan @lab nc.

This file collects collects the gaps between sequencial filenames and fill the gaps with file from
other folders.


"""

import glob
from shutil import copyfile
filelist = sorted(glob.glob('~/pva-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages/*.jpg'))
Pre = 0
Nex = 0
PreList = []
NexList = []


# Find the gaps
for idx, item in enumerate(filelist):
    
    Pre = filelist[idx-1].lstrip('~/pva-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages/')
    Nex = item.lstrip('~/pva-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages/')
    Pre = Pre.rstrip('.jpg')
    Nex = Nex.rstrip('.jpg') 
    if int(Nex) - int(Pre) != 1 and int(Nex)-int(Pre) > 0:
        print(('Pre, ', Pre,'Nex, ', Nex))
        PreList.append(Pre)
        NexList.append(Nex)
        
with open('~/pva-faster-rcnn/data/VOCdevkit2007/VOC2007/ImageSets/broken.txt','w') as brockenstring:
    for pre,nex in zip(PreList, NexList):
        brockenstring.write(str(pre) + ' '+ str(nex)+"\n")
       
#        
#src_pic_list  = sorted.glob.glob('/home/pohsuanh/Documents/Marathon2017/data/JPEGImages/TrainSet5/*.jpg')
#src_xml_list =  sorted.glob.glob('/home/pohsuanh/Documents/Marathon2017/data/Annotations/TrainSet5/*.xml')        
#PreNexList = zip(PreList, NexList)  
#print len(PreNexList)  
## Copy files and put them to the unfilled names in the dst folder.  
#for k in PreNexList:        
#    for code in range( int(k[0]) +1, int(k[1])):
#        src_pic = src_pic_list.pop(0)
#        src_xml = src_xml_list.pop(0)
#        newName = '{:07d}'.format(code) 
#
#        dst_pic =  '/home/pohsuanh/Documents/Marathon2017/data/JPEGImages/TrainSet5/' + newName+ '.jpg'
#        dst_xml = '/home/pohsuanh/Documents/Marathon2017/data/Annotations/TrainSet5/' + newName + '.xml'
#        copyfile( src_pic, dst_pic)
#        copyfile(src_xml, dst_xml)
#        
##%%
## concatenate the rest files to the end of the list
#code = filelist[-1]
#code = code.lstrip('/home/pohsuanh/Documents/Marathon2017/data/Annotations/TrainSet5/')
#code = code.rstrip('.xml')
#code = int(code)
#while  src_pic_list:
#        src_pic = src_pic_list.pop(0)
#        src_xml = src_xml_list.pop(0)
#        newName = '{:07d}'.format(code) 
#        print newName
#        dst_pic =  '/home/pohsuanh/Documents/Marathon2017/data/JPEGImages/TrainSet5/' + newName+ '.jpg'
#        dst_xml = '/home/pohsuanh/Documents/Marathon2017/data/Annotations/TrainSet5/' + newName + '.xml'
#        copyfile( src_pic, dst_pic)
#        copyfile(src_xml, dst_xml)
#        code +=1
#
#print 'finished'
#
#    

