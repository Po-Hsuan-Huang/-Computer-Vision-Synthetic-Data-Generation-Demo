#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:25:13 2017

@author: po-hsuan
"""

import cv2
from PIL import Image, ImageDraw
import numpy as np
from skimage.transform import ProjectiveTransform, warp
from matplotlib import pyplot as plt

def img_transform(img):
    '''
    perform image transform to the tag image.
    First, the image is affined transformed, and then perspetive transformed.
    
    parameters: 
            img: PIL image
                input image
    return:
            output_img : PIL image
            
            coeffs : 8-tuple
                coeffs of perspective transformation
                
            pos : 8-tuple 
                registering the final position of the verticies of the image
                
    '''
    
    # Affine transform
    width, height = img.size

    # perspective transform
    range_n = width*0.2
    
    # rand_degree() generates random points, the following vertices are the 
    # resulting vertices after transformation.
    
    x1 = np.random.uniform(0,range_n)
    y1 = np.random.uniform(0,range_n)
    
    x2 = np.random.uniform(width-range_n,width)
    y2 = np.random.uniform(0,range_n)
    
    x3 = np.random.uniform(width-range_n,width)
    y3 = np.random.uniform(height-range_n,height)
    
    x4 = np.random.uniform(0,range_n)
    y4 = np.random.uniform(height-range_n,height)
        
    dst = np.array(((x1, y1), (x2, y2), (x3, y3), (x4, y4)), dtype=np.float32)
    
    
    src = np.array(((0, 0),
                    (width, 0),
                    (width, height),
                    (0, height)),
                    dtype=np.float32)

        
    coeffsMatrix =  cv2.getPerspectiveTransform( src, dst)
    
    img = np.array(img)
    img = cv2.warpPerspective( img, coeffsMatrix, (width, height))
    img = Image.fromarray(np.uint8(-(img)*255))
    img.resize((width,height))
    
    # there is a resize to (width, height.) the resize ratio must be applied to bounding box of text ?
#    img = img.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
  
    # return the resulting verticies of the input image for bounding box transform.
    pos = ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
    
    return img, coeffsMatrix, pos



def bndbox_transform(in_box_pos, coeffsMatrix):
    '''
    the function transform the four-tuple position of the boudning box
    according to the transform function defined above. Meaning, 
    doing the affine transform first, and then do the perspective transform.
    
    The function sets the coordinate opposite to PIL convention:
        x -> -x
        y -> -y
    parameters:
        in_box_pos : 4-tuple
            position of the bounding w.r.t the tag image
            
        coeffs : 8-tuple
            coefficients of the perspective transformation used on tag img.

    return : 
        out_box_pos : 4-tuple
            location of the bounding box after transform
    '''

    # Affine transform  
    
    # top left point
    x0 = in_box_pos[0]
    y0 = in_box_pos[1]
    # bottom right point
    x2 = in_box_pos[2]
    y2 = in_box_pos[3]
    
    u0 = (x0, y0)
    u1 = (x2, y0)
    u2 = (x2, y2)
    u3 = (x0, y2)
    
    src = np.array([(u0, u1, u2, u3)], dtype = np.float32)
    dst = np.zeros(src.shape, dtype = np.float32)
    dst = cv2.perspectiveTransform( src, coeffsMatrix)
    #  return a rectangle that bounds the distorted bnd box.

    u0, u1, u2, u3 = dst[0]
    
    #left bound 
    left = min(u0[0], u3[0])
    #right bound
    right = max(u1[0], u2[0])
    #top bound
    top = min(u0[1], u1[1])
    #bottom bound
    bottom = max(u2[1], u3[1])
    
#    return (new_x0, new_y0, new_x1, new_y1)
    return (left, top, right, bottom)
