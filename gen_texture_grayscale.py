#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:24:02 2017

@author: po-hsuan


texture_alpha_template_converter 

The function converts random JPEG, PNG images into grayscale images.

The output image then later can be used as alpha maps. 
"""
from PIL import Image, ImageOps
from skimage import io
import glob, os


def gen_gray():
    image_list = glob.glob('./templates/*_alpha*.*')
    for img_path in image_list:
        # extract the file name from the file path
        fileplace, filename = os.path.split(img_path)
        filename = filename.rstrip('.jpg')
        filename = filename.rstrip('.jpeg')
        filename = filename.rstrip('.png')

        print(filename)
        image = Image.open(img_path)
        if image.mode != 'L':
            image = image.convert(mode = 'L')
            io.imsave('./alpha_texture/'+ filename +'.jpg', image)


def gen_inverted_gray():
    
    image_list = glob.glob('./templates/*_alpha*.*')
    for img_path in image_list:
        # extract the file name from the file path
        fileplace, filename = os.path.split(img_path) 
        filename = filename.rstrip('.jpg')
        filename = filename.rstrip('.jpeg')
        filename = filename.rstrip('.png')

        image = Image.open(img_path)
        if image.mode != 'L':
            image = image.convert(mode = 'L')
            
        image = ImageOps.invert(image)
        io.imsave('./alpha_texture/'+ 'inverted_'+ filename + '.jpg', image)

if __name__ == '__main__':
    
#    gen_gray()
    gen_inverted_gray()
    
    