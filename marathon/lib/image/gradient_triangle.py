#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:12:41 2017

@author: po-hsuan
"""


'''cropping test'''

from PIL import Image, ImageDraw
import numpy as np
import math
import random


''' Other functions---------------------------------------------------'''
def apply_black_gradient(input_im,
                         gradient = 1., initial_opacity=1.):
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
    output_im = Image.alpha_composite(input_im, black_im)

    return output_im
d



if __name__ == '__main__':
    
    temp = Image.open('./templates/03p.png')
    
    if temp.mode != 'RGBA':
        temp.convert('RGBA')
           
    temp_w= temp.size[0]
    temp_h= temp.size[1]
    
    screen = Image.new('RGBA', (2*temp_w, 2*temp_h), color = (256,256,256,256 ))
    
    screen_w = screen.size[0]
    screen_h = screen.size[1]
    
    mask = screen.copy()

    num_leaf = 1

    for i in range(num_leaf):
        mask_copy = mask.copy()
        leaf = Image.new('RGBA', (int(2.*temp_w), int(2*temp_h)), color =0 )    
        step = np.random.uniform(1.,3.,1)
        leaf = apply_black_gradient(leaf, step , 0.8 )

        # rotation angle of the gradient leaf. positive when rotate clockwise.    
        rotation_angle = -(np.random.randint(0,180))
        print i

        leaf = leaf.rotate(rotation_angle, expand =0)
        
#        leaf_pos = ( screen_w/2 - temp_w/2, screen_h/2 - temp_h/2 )
        # paste leaf at the side 
        mask_copy.paste(leaf, (0, 0))

        mask = Image.alpha_composite(mask, mask_copy)
        d = ImageDraw.Draw(mask_copy)
        d.rectangle(( screen_w/2 - temp_w/2 , screen_h/2 - temp_h/2, screen_w/2 + temp_w/2, screen_h/2 + temp_h/2),fill= None, outline=(256,0,0,256))
    
    # paste template at the center of the screen
    
    screen.paste(temp,( screen_w/2 - temp_w/2, screen_h/2 - temp_h/2))
    alpha = mask.split[-1]
    mask = mask.putalpha(alpha)
    print screen.mode, mask.mode
    screen = Image.alpha_composite(screen, mask)
    
    mask_copy.show()
    screen.show()
