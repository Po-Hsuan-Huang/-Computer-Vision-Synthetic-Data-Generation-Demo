#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:33:42 2017

@author: pohsuanh

rename files by a certain pattern

"""
import os, glob

#%%

os.chdir('/home/pohsuanh/disk1/Marathon/testImages/')
print((os.getcwd()))
files = glob.glob(os.getcwd()+"/*.jpg")
print  (files)
for i , afile in enumerate(files):
    code = i  +  1
    filename = '{:07d}'.format(code) 

    os.rename(afile, filename +'.jpg') 
    print(('filename :', filename))
    
    
#%%
import os, glob
#os.chdir('/home/pohsuanh.huang/pva-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages/50k/')
os.chdir('/home/pohsuanh/Desktop/test/')

print((os.getcwd()))
files = glob.glob(os.getcwd()+"/*.jpg")
print  (files)
for i , afile in enumerate(files):
    code = afile 
#    [f,g] = code.split('_')
#    filename = '{:07d}'.format( int(float( f + g ))) 
    filename = '{:07d}'.format( i + 1 ) 

    os.rename( afile, filename +'.jpg') 
    print(('filename :', filename))
    

