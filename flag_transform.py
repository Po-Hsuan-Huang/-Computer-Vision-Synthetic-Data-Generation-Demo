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

def find_linspace_index(x,y,lin_rows,lin_cols):
    print(('linrows', lin_rows))
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
#    print 'inline ', lin_rows[index_x], lin_cols[index_y]
    return index_x, index_y 
    
def find_map_index(x,y, rows, cols):
    '''
    return the index of the cooridnate in a warping map
    
    the warping matrix is defined as the following
    src_cols = np.linspace(0, cols, 20)
    src_rows = np.linspace(0, rows, 10)
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


def img_transform(image):
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
    # Sine wave parameters
    global pad_y_up
    sin_amp = 50
    sin_f =  np.random.uniform(0, 1)
    sin_ph = np.random.uniform(-np.pi/2, np.pi/2)
    sin =  np.sin(np.linspace(0, sin_f*np.pi, 20) + sin_ph) * sin_amp
    pad_y_up = max(0, int(round(np.max((sin)))) )
    pad_y_bot = np.abs(min(0, int(round(np.min((sin)))) ))
    pad_y_up  = 50 
    pad_y_bot = 50
    #load img
#    image = data.astronaut()
#    image = Image.open('./templates/06p.png')
#    image = np.array(image)
    
    #pad img
    image = np.pad(image, ((pad_y_up, pad_y_bot),(0,0),(0,0)), 'constant', constant_values=((0,0),(0,0),(0,0)))
    
    rows, cols = image.shape[0], image.shape[1]
    
    src_cols = np.linspace(0, cols, 20)
    src_rows = np.linspace(0, rows, 10)
    src_cols, src_rows = np.meshgrid(src_rows, src_cols) #convention of the meshgrid is transpose 
    
    src = np.dstack([src_rows.flat, src_cols.flat])[0]
    # before
#    plt.figure()
#    plt.plot(src[:, 0], src[:, 1], '.y')
#    label_pos_x = np.hstack( ( np.linspace(100,300,10), np.linspace(100,300,10)))
#    label_pos_y = np.hstack( ( np.linspace(100,100,10), np.linspace(300,300,10)))
#    x, y = np.meshgrid(label_pos_x, label_pos_y) 
#    plt.plot(x,y,'.b')
#    plt.imshow(image)
   
    # add sinusoidal oscillation to row coordinates
#    sin =  np.sin(np.linspace(0, sin_f*np.pi, 20) + sin_ph) * sin_amp
    shift = np.repeat(sin,10)
    #shift = np.hstack((sin,)*10)
    dst_rows = src[:, 0] 
    dst_cols = src[:, 1] -shift
    
    dst = np.vstack([dst_rows, dst_cols]).T
    
    
    tform = PiecewiseAffineTransform()
    tform.estimate(src, dst)
    
    out_rows = image.shape[0]
    out_cols = cols
    out = warp(image, tform, output_shape=(out_rows , out_cols))
    
        
#    rescale image from [0,1] to [0, 255]
    out = Image.fromarray(np.uint8(out*255))
    # format the numpy array to image data format
#    pixels = list(tuple(pixel) for pixel in out)
#    output_img = Image.fromarray(np.uint8(pixels))
    return out, tform

def bndbox_transform(label_pos, tform):
    global pad_y_up
    x_min = label_pos[0]
    y_min = label_pos[1] + pad_y_up
    x_max = label_pos[2]  
    y_max = label_pos[3] + pad_y_up
#%% bounding lines
    label_pos_x = np.array((x_min, x_max, x_min, x_max))
    label_pos_y = np.array((y_min, y_min, y_max, y_max))
    
    label_rows, label_cols = np.meshgrid(label_pos_x, label_pos_y)
    label = np.dstack([label_rows.flat, label_cols.flat])[0]

    

    dst_rows, dst_cols = tform.inverse(label)[:, 0], tform.inverse(label)[:, 1]

    #left bound
    left = min(dst_rows)
    #right bound
    right = max(dst_rows)
    #top bound
    top = min(dst_cols)
    #bottom bound
    bottom = max(dst_cols)
    
    # in real cooridate, row and colmn is the opposite
    return  (left, top, right, bottom) #, dst_label
    

if __name__ == '__main__':  
    
    image = data.astronaut()

    label_pos = [  100, 100, 300, 300]
    
    out, tform =transfrom(image)
    
    dst_label = bndbox_transfrom(label_pos, tform)
    
    (left,top,right,bottom)= dst_label
    
    fig, ax = plt.subplots()
    
    #    left, top, right, bottom = newPos
    ax.imshow(out)
    
    d = ImageDraw.Draw(out)
    
    d.line((left, top, right, top), fill=(255,0,255,255), width=4)
    d.line((right, top, right, bottom), fill=(255,0,255,255), width=4)
    d.line((right, bottom, left, bottom), fill=(255,0,255,255), width=4)
    d.line((left, bottom, left, top), fill=(255,0,255,255), width=4)



    # line transformed
    label_pos_x = np.hstack( ( np.linspace(100,300,10), np.linspace(100,300,10)))
    label_pos_y = np.hstack( ( np.linspace(100,100,10), np.linspace(300,300,10)))
    x, y = np.meshgrid(label_pos_x, label_pos_y) 
    tline = np.dstack([x.flat, y.flat])[0]
    plt.plot(tform.inverse(tline)[:, 0], tform.inverse(tline)[:, 1] ,'.b')
    ax.imshow(out)
