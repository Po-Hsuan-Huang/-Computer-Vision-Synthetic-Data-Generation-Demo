#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 15:44:29 2017

@author: pohsuanh
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:38:37 2017

"""

from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
from skimage import data
import random

def find_linspace_index(x,y,lin_rows,lin_cols):
#    print 'linrows', lin_rows
    print(('atual, ', x, y)) 
    # find the nearest elemet to x, y in the linspaces
    if np.where(lin_rows > x)[0].any():
        index_x = np.where(lin_rows > x)[0][0]
    else :
        index_x = lin_rows[-1]
        
    if np.where(lin_cols > y)[0].any():
        index_y = np.where(lin_cols > y)[0][0]
    else :
        index_y = lin_cols[-1]
#    print 'indices, ', index_x, index_y
    print(('inline ', lin_rows[index_x], lin_cols[index_y]))
    return index_x, index_y 
    
def find_map_index(x,y, rows, cols):
    '''
    return the index of the cooridnate in a warping map
    
    the warping matrix is defined as the following
    src_cols = np.linspace(0, cols, 20)
    src_rows = np.linspace(0, rows, 20)
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    
    parameters:
        x, y : int  
          the coordinate before warping
        
        cols, rows : the shape of the image before warping
    return: 
        x_new, y_new :
         the coordinate after warping

    '''
  
    return rows * y + x


def transfrom(image):
    '''
        The function transform the imput rectangular image into sinusoidal
        wave geomatry in x direction. It mimics the effect of flag in the wind.
        The frequency and the starting location of the image can be adjusted 
        by changing 'frequency' and 'offset' 
        
        note : the algorithm is kind of slow to put pixel back from numpy array to image data.
        
        parameters:
            image : PIL image
        
        
        return :
            output_img : PIL image
        
        
    '''
#i
    image = np.array(image)
    image = np.transpose(image, (1,0,2))
    rows, cols = image.shape[0], image.shape[1]
    
    # create meshgrid coordinate
    lin_cols = np.linspace(0, cols, 20)
    lin_rows = np.linspace(0, rows, 10)
    src_rows, src_cols = np.meshgrid(lin_rows, lin_cols)
    src = np.dstack([src_rows.flat, src_cols.flat])[0]
    
    
    
    # add sinusoidal oscillation to row coordinates
    
    offset = 0 #random.uniform(0, np.pi) 
    frequency = 1#random.uniform(0, 1.)
    dst_rows = src[:, 0] - 3*np.sin(np.linspace(0, frequency * np.pi, src.shape[0]) + offset) * 50
    dst_rows = float(rows)/(max(dst_rows)-min(dst_rows))  * (dst_rows - min(dst_rows)) 
    dst_cols = src[:, 1] 
   
    # Enlarge and shift the position of the image to make its coordinate >= 0 
    # oscillate amplitude is 50 pixels.
    
    dst_rows *= 1. 
#    dst_rows -= 1. * 50
    
    dst = np.vstack([dst_cols, dst_rows]).T
#    dst = np.vstack([dst_rows, dst_cols]).T

    # create mapping for warpping
    tform = PiecewiseAffineTransform()
    tform.estimate(src, dst)
    out_rows = image.shape[0]
    out_cols = cols
    out = warp(image, tform.inverse, output_shape=(out_rows, out_cols))
    
#    rescale image from [0,1] to [0, 255]
    out = out*255
    # format the numpy array to image data format
    pixels = list(tuple(pixel) for pixel in out)
    output_img = Image.fromarray(np.uint8(pixels))
    return output_img, frequency, tform

def bndbox_transfrom(frequency,label_pos, image):
    '''
        The function transform the imput rectangular image into sinusoidal
        wave geomatry in x direction. It mimics the effect of flag in the wind.
        The frequency and the starting location of the image can be adjusted 
        by changing 'frequency' and 'offset' 
        
        note : the algorithm is kind of slow to put pixel back from numpy array to image data.
        
        parameters:
        
            frequency: the frequency of oscillation
            
            label_pos : bounding box after transform
            
            image : PIL image to be transformed
        returhn:
            
            label_pos : 4-tuple
        
    '''
    image = np.array(image)
    rows, cols = image.shape[0], image.shape[1]
  
    
    # create meshgrid coordinate
    lin_cols = np.linspace(0, cols, 20)
    lin_rows = np.linspace(0, rows, 10)
    src_rows, src_cols = np.meshgrid(lin_rows, lin_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    
    # find the indices of the coordinates in linspace
    index_x = list(range( max( label_pos.shape)))
    index_y = list(range(len(index_x)))
    
    for i, (x, y) in enumerate (zip (label_pos[0], label_pos[1])):
        index_x[i], index_y[i] = find_linspace_index(x, y, lin_rows, lin_cols)   
    
    # find the indices in the warping map

    idx = list(range(len(index_x)))
    for i, (x, y) in enumerate (zip (index_x, index_y)):
        idx[i] = find_map_index( x, y, 20, 10)
     # add sinusoidal oscillation to row coordinates
    
    offset = 0 # random.uniform(0, np.pi)
    frequency = 1#random.uniform(0, 1.)
    dst_rows = src[:, 0] - 3 * np.sin(np.linspace(0, frequency * np.pi, src.shape[0]) + offset) * 50
    dst_rows = float(rows)/(max(dst_rows)-min(dst_rows))  * (dst_rows - min(dst_rows)) 
    dst_cols = src[:, 1] 
    
    # Enlarge and shift the position of the image to make its coordinate >= 0 
#    dst_rows *= 1.5 
#    dst_rows -= 1.5 * 50
    
    dst = np.vstack([dst_cols, dst_rows]).T
  # create mapping for warpping
 

#    u0 = np.roll (dst[idx[0], :], 1 )
#    u1 = np.roll (dst[idx[1], :], 1 )
#    u2 = np.roll (dst[idx[2], :], 1 )
#    u3 = np.roll (dst[idx[3], :], 1 )
#    u0 = dst[idx[0], :]
#    u1 = dst[idx[1], :]
#    u2 = dst[idx[2], :]
#    u3 = dst[idx[3], :]
    u = []
    for i in idx:
        u.append(dst[i])
    
    print(u)

    
#    dst_label = np.vstack((u0, u1, u2, u3))
 
    return u

if __name__ == '__main__':  
    
    label_pos = [  100, 100, 300, 300]
    label_pos_x = np.linspace(10,500,10)
    label_pos_y = np.linspace(200,200,10)
    label_pos = np.vstack([label_pos_x, label_pos_y])
    
    image = data.astronaut()
    
    image_trans, freq, tform = transfrom(image)
    
    dst_label = bndbox_transfrom( freq, label_pos, image)
    
    
#    left, top, right, bottom = newPos
    img = Image.fromarray(np.uint8(image_trans))
#    d = ImageDraw.Draw(img)
#    for a_x, a_y in dst_label:
#        for b_x, b_y in np.roll(dst_label,1):
#            d.line((a_x, a_y, b_x , b_y ), fill=(255,255,0,255), width=4)
    fig, ax = plt.subplots()
    dst_label = np.asarray( dst_label).T
    dst_label = np.reshape(dst_label,(2,-1))
    ax.plot( dst_label[0], dst_label[1], 'g*')
    
            
    ax.imshow(img)
    ax.plot(label_pos[0], label_pos[1],'r*')

#    ax.plot(left, top, 'r*')
#    ax.plot(right, bottom, 'b*')
    ax.axis((0, image.shape[1], image.shape[0], 0))
    plt.show()

#%%
