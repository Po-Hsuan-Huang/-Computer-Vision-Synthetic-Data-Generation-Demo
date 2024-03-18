#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:26:06 2017

@author: po-hsuan
"""

'''cropping test  
    I tried to test how does pasting gradient leaves on the template and crop it 
    looks like. The result shows I must implement the rotational center shift 
    algorithm to make it looks okay. 
    
    This algorithm is not really fast and create unnatural edges when the leaves 
    does not cover the whole image. The gradients should not apply on the whole
    template but only the fractals wih the right orientation. 



'''

from PIL import Image, ImageDraw, ImageChops
import numpy as np
import math
import random


#if __name__ == '__main__':

    
def draw_shade(imput_img, num_leaf, **kwargs):
    
    
    '''
    The function applies alpha channel shades on imput image.
    The function allows user to chose how many layers of shades to use.
    The shades are black alpha gradients sampling from 8 directions included
    inside leaf_name_dict.
    
    description of directions of shades.
    leaf_name_dict=     {'UL': upper left
                         'UR': upper right
                         'DL': down left
                         'DR': down right
                         'TL': true left
                         'TR': true right 
                         'TU': true up
                         'TD': true down}
    
    parameter:
        imput_img : PIL image
        num_leaf : number of shades to put on
        
        *kargs: 
            c : color of shades. Default is black (0.0)
                
    return: 
        output_img :PIL image 
    
    '''
    Color = 0 # default color
    Random_Color = False
    if kwargs is not None:
        for key, value in list(kwargs.items()): 
                key = value

        
    temp = imput_img    
    if temp.mode != 'RGBA':
        temp = temp.convert('RGBA')
           
    temp_w= temp.size[0]
    temp_h= temp.size[1]
    # Create new image as working space 
    screen = Image.new('RGBA', (4*temp_w, 4*temp_h), color = (256,256,256,256 ))
    mask = Image.new('L', screen.size, color = 0)

    screen_w = screen.size[0]
    screen_h = screen.size[1]
    
#    num_leaf = 2
    
    leaf_pos_center =(screen_w/2 - temp_w/2 ,screen_h/2 - temp_h/2)
    leaf_pos_shift_dict={'UL':( -1, -1),
                         'UR':( +1, -1),
                         'DL':( -1, +1),
                         'DR':( +1, +1),
                         'TL':( -1,  0),
                         'TR':( +1,  0), 
                         'TU':(  0, -1),
                         'TD':(  0, +1)}
    
    leaf_name_dict = ['UL', 'UR', 'DL', 'DR', 'TL', 'TR', 'TU', 'TD']
    leaf_rotation_angle_base = { 'UL': 0, 'UR': 0, 'DL': 90, 'DR': 90, 'TL': 45, 'TR': 45, 'TU': -45, 'TD': -45 }
    leaf_flip_base = { 'UL': None, 'UR': Image.FLIP_LEFT_RIGHT, 'DL': None, 'DR': Image.FLIP_LEFT_RIGHT, 'TL': None, 'TR': Image.FLIP_LEFT_RIGHT, 'TU': None, 'TD': Image.FLIP_TOP_BOTTOM }

    # draw samples 
    leaf_draw_list = random.sample( leaf_name_dict, num_leaf)
    
#    leaf_draw_list = ['UL']
    
    for i in leaf_draw_list:
        # leaf is a small patch of alpha that can be pasted on alpha mask
        if Random_Color:
            Color=np.random.choice([0,1])
            
        leaf = Image.new('L', (int(4*temp_w), int(4*temp_h)), color = Color )    
        step = np.random.uniform( 2., 2.5, 1)
        leaf = apply_black_gradient(leaf, step , 0.9 )

        # rotation angle of the gradient leaf. positive when rotate clockwise.    
        rotation_angle = -45 + leaf_rotation_angle_base[i] 
#        print i

        leaf = leaf.rotate(rotation_angle, expand =0)
        
        if leaf_flip_base[i] != None : 
            leaf = leaf.transpose(leaf_flip_base[i])
#        leaf_pos = tuple( np.asarray(leaf_pos_center) + np.asarray(leaf_pos_shift_dict['UL'])*np.array(temp.size)/2 )
        leaf_pos = (0,0)
        
        alpha_screen = Image.new('L', screen.size, color = 0 )

        alpha_screen.paste(leaf, leaf_pos)

        # paste leaf on the alpha mask 
        mask = ImageChops.add(mask, alpha_screen)
        
        
    #put alpha on the black image to create black shades      
    black_im = Image.new('RGBA', screen.size, color = 0 )#  color = 0 : black
    black_im.putalpha(mask)
    # paste template at the center of the screen
    screen.paste(temp,( int(screen_w/2 - temp_w/2), int(screen_h/2 - temp_h/2)))
    
    #composite screen and shades
    screen = Image.alpha_composite(screen, black_im)
    # crop the part where input_img is at
    cropbox = (screen_w/2 - temp_w/2, screen_h/2 - temp_h/2, screen_w/2 + temp_w/2, screen_h/2 + temp_h/2)
    output_img = screen.crop(cropbox)

    return output_img



''' Other functions---------------------------------------------------'''
def apply_black_gradient(input_im, gradient = 1., initial_opacity=1.):
    """
    Applies a black gradient to the image, going from left to right.

    Arguments:
    ---------
        input_im: image object
            an image object to be applied the graindet
        
        mask : a transparency mask (mode'1') or matte(mode'L','RGBA')
            the gradient will be drawn in this mask
        
        slope : slope of the given grandient.
        
        gradient: float (default 1.)
            gradient of the gradient; should be non-negative;
            if gradient = 0., the image is black;
            if gradient = 1., the gradient smoothly varies over the full width;
            if gradient > 1., the gradient terminates before the end of the width;
        initial_opacity: float (default 1.)
            scales the initial opacity of the gradient (i.e. on the far left of the image);
            should be between 0. and 1.; values between 0.9-1. give good results
    """

    # get image to operate on

    if input_im.mode != 'RGBA':
        input_im = input_im.convert('RGBA')
        
    width, height = input_im.size

    # create a gradient that
    # starts at full opacity * initial_value
    # decrements opacity by gradient * x / width
    alpha_gradient = Image.new('L', (width, 1), color = 0 )
    for x in range(width):
        a = int((initial_opacity * 255.) * (1. - gradient * float(x)/width))
        if a > 0:
            alpha_gradient.putpixel((x, 0), a)
        else:
            alpha_gradient.putpixel((x, 0), 0)
        # print '{}, {:.2f}, {}'.format(x, float(x) / width, a)
    alpha = alpha_gradient.resize(input_im.size)
    # create black image, apply gradient
    black_im = Image.new('RGBA', (width, height), color=0) # i.e. black
    black_im.putalpha(alpha)
    # make composite with original image
#    output_im = Image.alpha_composite(input_im, black_im)

    return alpha


