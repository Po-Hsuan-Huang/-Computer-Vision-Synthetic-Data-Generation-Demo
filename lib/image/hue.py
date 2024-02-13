#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:46:53 2017

@author: pohsuan

Data Augmentation

"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob, os
from shutil import copyfile


if __name__=='__main__':

    initName = 750000
    imgNum = 10
    
    imgList = sorted(glob.glob('/home/pohsuan/disk1/Marathon/JPEGImages/TrainSet5/*jpg'))[13457:imgNum+13457]
    xmlList = sorted(glob.glob('/home/pohsuan/disk1/Marathon/Annotations/TrainSet5/*xml'))[13457:imgNum+13457]
     
    img_dst_path = '/home/pohsuan/disk1/Marathon/JPEGImages/TrainSet6/'
    xml_dst_path = '/home/pohsuan/disk1/Marathon/Annotations/TrainSet6/'
    
    Hue = False
    Saturation = False
    Value = False
    Blur = True
    
    for j , img in enumerate(imgList):
        
        xmltag = xmlList[j].lstrip('/home/pohsuan/disk1/Marathon/Annotations/TrainSet5/').rstrip('.xml')
        imgtag =imgList[j].lstrip('/home/pohsuan/disk1/Marathon/JPEGImages/TrainSet5/').rstrip('.jpg')
        print imgtag
        if xmltag == imgtag:
            
            
            img = cv2.imread(img)
#            img = cv2.imread('/home/pohsuan/disk1/Marathon/JPEGImages/TrainSet5/0400010.jpg')
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv2 = hsv.copy()
            if Hue :
                print 'Hue'
                # control hue
                hueMax = np.ones(img.shape[:2]) * 180
                hueMin = np.zeros(img.shape[:2])
                hue_bias = np.random.normal(0,90)  
                hue_map = np.fmin(( 0.8 * hsv[:,:,0] + 0.2 * np.ones(hsv.shape[:2]) * hue_bias), hueMax)
                hue_map = np.fmax(hue_map, hueMin)
                hsv2[:,:,0] = hue_map    
                
            if Saturation : 
                print 'Satur'
                # control saturation
                satMax = np.ones(img.shape[:2]) * 255
                satMin = np.zeros(img.shape[:2])
                sat_bias = np.random.normal(0,64)  
                sat_map = np.fmin(( 0.8 * hsv[:,:,1] + 0.2 * np.ones(hsv.shape[:2]) * sat_bias), satMax)      
                sat_map = np.fmax(sat_map, satMin)
                hsv2[:,:,1] = sat_map  
                
            if Value :
                print 'value'
                # control brightness
                valMax = np.ones(img.shape[:2]) * 255
                valMin = np.zeros(img.shape[:2])
                val_bias = np.random.normal(0,64)  
                val_map = np.fmin(( 0.8 * hsv[:,:,2] + 0.2 * np.ones(hsv.shape[:2]) * val_bias), valMax)
                val_map = np.fmax(val_map, valMin)
                hsv2[:,:,2] = val_map      
        
            if Blur :
               print 'blur'
               # control ))
               kx = np.random.randint(5,10)
               ky = np.random.randint(5,10)
               ksize = (kx,ky)
               hsv2 = cv2.blur(hsv2, ksize)
            if Contrast :
                print 'Contrast'
                
                
            new_img =  cv2.cvtColor(hsv2.astype(np.uint8) , cv2.COLOR_HSV2RGB)
            plt.figure(figsize=(15,15))
            plt.imshow(new_img)
#    
#            filename = '{:07d}'.format(initName+j)
    
#            plt.imsave(img_dst_path + filename +'.jpg', new_img)
    
#            copyfile(xmlList[j], xml_dst_path + filename +'.xml')
        else :
            print 'discontinoity in filenames : ', imgtag
            xmlList.insert(j,'NAL')