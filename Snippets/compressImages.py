#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:59:28 2017

@author: pohsuanh

compress images by JPEG compression 

"""
from skimage import util, img_as_float, io
import glob
import cv2

img_dst_path = os.path.join(os.path.getcwd(),'/JPEGImages/TrainSet6/uplaoddir/'
imgList = sorted(glob.glob(os.path.join(os.path.getcwd(),'/JPEGImages/TrainSet5/uplaoddir/*jpg'))
#imgList = (glob.glob('/home/pohsuanh/Documents/Marathon2017/*jpg'))

for i, src_path in enumerate(imgList):
    img=cv2.imread(src_path)
    io.imsave(src_path, img, quality = 15 )
    