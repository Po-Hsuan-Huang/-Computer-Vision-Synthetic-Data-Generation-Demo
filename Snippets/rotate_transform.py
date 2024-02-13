#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:02:27 2017

@author: pohsuan
"""

from skimage import data
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt


#%% 
def img_transform(image, angle):
    global PADDING
    
    pad = max(PADDING, 0) 
    image = np.pad(image, ((pad, pad),(pad,pad),(0,0)), 'constant', constant_values=((0,0),(0,0),(0,0)))
    image = Image.fromarray(np.uint8(image))
    image = image.rotate(angle)
    return image

#%% rotate bounding box
def bndbox_transform(vertex, rot_center, angle, resize = 1):
    """
    vertex : 4 tuple
        vertices of the bndbox
    rot_center: 2 tuple
        center of roation
    angle : in degree
    
    """
    global PADDING    
    pad = max(PADDING, 0) 
    pad_origin = np.array([pad,pad])
    vectors = vertex - rot_center  
    degree = -(angle*np.pi/180)
    rotate_matrix = np.asanyarray([[np.cos(degree), -np.sin(degree)], [np.sin(degree), np.cos(degree)]])
    rot_vectors = np.dot(rotate_matrix, np.asarray(vectors.T))
    rot_vertex = rot_vectors.T + rot_center + pad_origin
    rot_vertex *= resize

    left = min(rot_vertex.T[0])
    right = max(rot_vertex.T[0])
    top = min(rot_vertex.T[1])
    bottom = max(rot_vertex.T[1])
    bndbox =  (left,right,top,bottom)
    
    return rot_vertex, bndbox
def set_pad(pad):
    global PADDING
    PADDING = pad



if __name__ == '__main__':
    image = data.astronaut()
    image = Image.fromarray(np.uint8(image))
    size = image.size
    
    
    
    #%% draw bounding box on image
    label_pos_x = np.hstack( ( np.linspace(300,400,2), np.linspace(300,400,2)))
    label_pos_y = np.hstack( ( np.linspace(300,300,2), np.linspace(400,400,2)))
    label_rows, label_cols = np.meshgrid(label_pos_x, label_pos_y)
    label = np.dstack([label_rows.flat, label_cols.flat])[0]

    
    left = min(label_pos_x)
    right = max(label_pos_x)
    top = min(label_pos_y)
    bottom = max(label_pos_y)
    vertex = np.meshgrid((left,right),(top,bottom)) 
    vertex = np.reshape(np.asarray(vertex).T, [4,2])  
    
    d = ImageDraw.Draw(image)
    
    d.line((left, top, right, top), fill=(255,0,255,255), width=4)
    d.line((right, top, right, bottom), fill=(255,0,255,255), width=4)
    d.line((right, bottom, left, bottom), fill=(255,0,255,255), width=4)
    d.line((left, bottom, left, top), fill=(255,0,255,255), width=4)
 
#%% do_transform
  
    set_pad(100)
    angle = 20
    org_size = image.size
    rot_center = (image.size[0]/2, image.size[1]/2)    
    img = img_transform(image, angle)
    rot_size = img.size
    resize = [ float(b)/a for a,b in zip(rot_size , org_size)]
#    image.thumbnail(org_size)
    vertex , bndbox = bndbox_transform(vertex, rot_center, angle)

    fig, ax = plt.subplots(figsize=(8, 8))
    
    ax.plot(label_rows , label_cols , '.c' )
        
    ax.imshow(img)

    ax.plot( vertex.T[0], vertex.T[1], '.w')
    
    points = np.meshgrid((bndbox[0], bndbox[1]), (( bndbox[2]), bndbox[3]))
    points = np.reshape(np.asarray(points).T, [4,2])  

    ax.plot( np.array(points).T[0], np.array(points).T[1], '.g')

    
    