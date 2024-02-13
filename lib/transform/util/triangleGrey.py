#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 11:30:13 2017

@author: po-hsuan
"""
from PIL import Image, ImageDraw
import numpy as np

   

def draw_shade(img, mode):
    ''' Draw triangles with random shades of greys on the input image.
    
        img: image object    
    
        mode: string
            'octagon': draw triangles on each corner of the input image 
                
            'triangle': draw on triangle on the input image                    
        
    '''
    img_size_w, img_size_h = img.size
    shade = Image.new('RGBA', img.size, (0,0,0,0)) #transparent 

    # octagonal mask
    if mode =='octagon':
#        opaque = np.random.randint(25,221)
        opaque = 125
        m = np.random.sample(4) * 0.6 *img_size_w
        n = np.random.sample(4) * 0.6 *img_size_h
        # vertices on top and botton sides
        M = list(zip( [ m[0], img_size_w -m[1], img_size_w - m[2], m[3]  ],
                [ 0, 0, img_size_h, img_size_h] ))
       # vertices on left and right sides
        N = list(zip([0, img_size_w, img_size_w, 0], 
                [n[0], n[1], img_size_h - n[2], img_size_h - n[3]]))
    
        shadeColor = (0,0,0,256)
    
        ''' octgonal shades'''
        piece1 = Image.new('RGBA', img.size, color=0) # no color
        piece2 = piece1.copy()
        piece3 = piece1.copy()
        piece4 = piece1.copy()
        
        draw1 = ImageDraw.Draw(piece1)
        draw2 = ImageDraw.Draw(piece2)
        draw3 = ImageDraw.Draw(piece3)
        draw4 = ImageDraw.Draw(piece4)
        
        draw1.polygon(((0,0),M[0],N[0]), fill=shadeColor)
        draw2.polygon(((img_size_w, 0),M[1],N[1]), fill =shadeColor)
        draw3.polygon(((img_size_w,img_size_h),M[2],N[2]), fill=shadeColor)
        draw4.polygon(((0,img_size_h),M[3],N[3]), fill=shadeColor)


        piece1 = apply_black_gradient(piece1,1,0.9)
        piece2 = apply_black_gradient(piece2,2,0.8)
        piece3 = apply_black_gradient(piece3,3,0.7)
        piece4 = apply_black_gradient(piece4,1,0.6)
        
        print((shade.mode, shade.size))
        print((piece1.mode, piece1.size))
        
        
        shade = Image.alpha_composite( shade, piece1)
        shade = Image.alpha_composite( shade, piece2)
        shade = Image.alpha_composite( shade, piece3)
        shade = Image.alpha_composite( shade, piece4)
        shade.save('templates/alpha_composite.png')
        
        
    if mode =='triangle':
        V = [(0,0),(img_size_w, 0),(img_size_w,img_size_h),(0,img_size_h)]
       
        s0,s1,s2 = np.random.choice(list(range(12)),3)
        # flatten the lists of all vertices of triangles, and randomly choose 3
        T = V+M+N
        
        d = ImageDraw.Draw(shade)
        d.polygon((T[s0], T[s1], T[s2]), fill = shadeColor)
        
        return shade

 

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
    alpha_gradient = Image.new('L', (width, 1), color=0xFF)
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