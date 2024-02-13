#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 11:45:32 2017

@author: pohsuan

Draw Hue, Saturation, and Intensity
"""
import  cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageEnhance, Image,ImageFilter

def Hue(img) :
#    print 'Hue'
    # control hue
#    hueMax = np.ones(img.shape[:2]) * 180
#    hueMin = np.zeros(img.shape[:2])
#    hue_bias = np.random.uniform(-180,180)  
#    hue_map = np.fmin((  hsv[:,:,0] + np.ones(hsv.shape[:2]) * hue_bias), hueMax)
#    hue_map = np.fmax(hue_map, hueMin)
#    hsv2[:,:,0] = hue_map
#    new_img =  cv2.cvtColor(np.asarray(hsv2) , cv2.COLOR_HSV2RGB)
    
    factor= np.random.uniform(0,2)
    enhencer = ImageEnhance.Color(img)
    hsv2 = enhencer.enhance(factor)    
    return hsv2

def Saturation(img) : 
#    print 'Satur'
    # control saturation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    satMax = np.ones(img.shape[:2]) * 255
    satMin = np.zeros(img.shape[:2])
    sat_bias = np.random.uniform(-30,10)  
    sat_map = np.fmin((  hsv[:,:,1] + np.ones(hsv.shape[:2]) * sat_bias), satMax)      
    sat_map = np.fmax(sat_map, satMin)
    hsv2[:,:,1] = sat_map  
    new_img =  cv2.cvtColor(np.asarray(hsv2) , cv2.COLOR_HSV2RGB)

    return hsv2

def Brightness(img) :
#    print 'value'
    # control brightness
#    valMax = np.ones(img.shape[:2]) * 255
#    valMin = np.zeros(img.shape[:2])
#    val_bias = np.random.uniform(-64,64)  
#    val_map = np.fmin((  hsv[:,:,2] + np.ones(hsv.shape[:2]) * val_bias), valMax)
#    val_map = np.fmax(val_map, valMin)
#    hsv2[:,:,2] = val_map   
#    new_img =  cv2.cvtColor(np.asarray(hsv2) , cv2.COLOR_HSV2RGB)

#    factor= np.random.uniform(0.7,1.5)
    factor = np.random.randn(1)*0.2 + 1
    enhencer = ImageEnhance.Brightness(img)
    hsv2 = enhencer.enhance(factor)
    return hsv2


def Sharpness(img) :
#    print 'blur'
    factor= np.random.randn(1)*2 - 2.3
    enhencer = ImageEnhance.Sharpness(img)
    hsv2=enhencer.enhance(factor)
    hsv2 =  img.filter(ImageFilter.GaussianBlur(radius=factor))
    return hsv2

def Contrast(img) :
    '''
    actor – A floating point value controlling the enhancement.
    Factor 1.0 always returns a copy of the original image, 
    lower factors mean less color (brightness, contrast, etc), 
    and higher values more. There are no restrictions on this value.
    '''
#    print 'Contrast'
    factor= np.random.randn(1)*0.2 + 1 
    enhencer = ImageEnhance.Contrast(img)
    hsv2=enhencer.enhance(factor)
    return hsv2
 
  

if __name__ == '__main__':
    img = Image.open('/home/pohsuan/Documents/Marathon2017/templates/03.png')
    hsv2 = img.copy()
#    hsv2 = Hue(hsv2)
#    hsv2 = Brightness(hsv2)
#    hsv2 = Contrast(hsv2)
    hsv2 = Sharpness(hsv2)
    plt.figure(figsize=(10,10))
    plt.imshow(hsv2)