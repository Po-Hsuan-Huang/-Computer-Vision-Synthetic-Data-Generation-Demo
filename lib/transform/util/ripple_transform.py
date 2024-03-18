#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 16:46:05 2017

@author: pohsuanh
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:38:37 2017

"""
import os
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
from skimage import data

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
    global pad_left
    img_x, img_y = image.size
    sin_amp = np.random.normal(50,20)
    sin_ph = np.random.uniform(0, np.pi)
    f = np.random.uniform(0,1)
    sin =  np.sin(np.linspace( sin_ph, f*np.pi + sin_ph, 20) ) * sin_amp
#    plt.plot(sin)
    pad_left = 0
    pad_right = int(sin[-1]) if sin[-1] >= 0 else 0
    image = np.pad(image, ((0, 0),(pad_left, pad_right),(0,0)), 'constant', constant_values=((0,0),(0,0),(0,0)))

    #load img
#    image = data.astronaut()
#    image = Image.open('./templates/06p.png')
#    image = np.array(image)
    
    #pad img    
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
#    sin =  np.sin(np.linspace(0, sin_f*np.pi, 20) ) * sin_amp
    shift = np.repeat(sin,10)
    #shift = np.hstack((sin,)*10)
    dst_rows = src[:, 0] + shift
    dst_cols = src[:, 1] #-shift
    
    dst = np.vstack([dst_rows, dst_cols]).T
    
    
    tform = PiecewiseAffineTransform()
    tform.estimate(dst, src)
    
    out_rows = image.shape[0]
    out_cols = cols
    out = warp(image, tform, output_shape=(out_rows , out_cols))
    
#     plt.figure()
#     dst_rows, dst_cols = tform.inverse(src)[:, 0], tform.inverse(src)[:, 1]

#     plt.plot(dst_rows, dst_cols,'.y')
#    #left, top, right, bottom = newPos
#     plt.xlim((0,int(img_x)))
#     plt.ylim((0,int(img_y)))
#     plt.imshow(out)

#    rescale image from [0,1] to [0, 255]
    out = Image.fromarray(np.uint8(out*255))
    # format the numpy array to image data format
#    pixels = list(tuple(pixel) for pixel in out)
#    output_img = Image.fromarray(np.uint8(pixels))

    return out, tform

def bndbox_transform(label_pos, tform):
    global pad_left
    x_min = label_pos[0] + pad_left
    y_min = label_pos[1] 
    x_max = label_pos[2] + pad_left
    y_max = label_pos[3] 
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
    global pad_left
    image = data.astronaut()
    image = Image.open(os.path.join(os.getcwd(),'templates/03.png'))
    label_pos = [  100, 100, 300, 300]
    
    out, tform =img_transform(image)
    
    dst_label = bndbox_transform(label_pos, tform)
    
    (left,top,right,bottom)= dst_label
    
    fig, ax = plt.subplots()
    #    left, top, right, bottom = newPos
    ax.imshow(out)
    
    d = ImageDraw.Draw(out)
    
    d.line((left, top, right, top), fill=(255,0,255,255), width=4)
    d.line((right, top, right, bottom), fill=(255,0,255,255), width=4)
    d.line((right, bottom, left, bottom), fill=(255,0,255,255), width=4)
    d.line((left, bottom, left, top), fill=(255,0,255,255), width=4)



#    # line transformed
#
    label_pos_x = np.hstack( ( np.linspace(100+ pad_left,300 + pad_left,10), np.linspace(100+ pad_left,300 + pad_left,10)))
    label_pos_y = np.hstack( ( np.linspace(100,100,10), np.linspace(300,300,10)))
    x, y = np.meshgrid(label_pos_x, label_pos_y) 
    tline = np.dstack([x.flat, y.flat])[0]
    plt.plot(tform.inverse(tline)[:, 0], tform.inverse(tline)[:, 1] ,'.b')
    plt.imshow(out)
    plt.show()
