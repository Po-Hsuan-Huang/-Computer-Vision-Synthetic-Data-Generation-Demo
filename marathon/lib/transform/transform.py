#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 17:52:13 2017

@author: pohsuan

Class of all geometrical transform functions

There are four types of transforms : 'rotation', 'flag', 'ripple', 'perspective'
                    

"""

from submodules import flag_transform, perspective_transform, rotate_transform, ripple_transform
import numpy as np    

'''
Parameters:
   
    bndbox : 6-tuple 
        
        code_x, code_y : pos of text
       
        CodeWidth_En, CodeHeight_En : Shape of the English alphabet of the text 
       
        CodeWidth_Nb, CodeHeight_Nb : Shape of the last 5 digit of the text
   
    img : original image

        
return : 
    img_out: transformed image
    
    newPos : transformed bndbox 

'''
    
def perspective( img, bndboxs) :
    newPos = []
    

    img_out, coeffs, pos = perspective_transform.img_transform(img) 
    
    newPos = [ perspective_transform.bndbox_transform(bndbox, coeffs ) for bndbox in bndboxs]

    return img_out , newPos
    
    
    
def flag(img, bndboxs):
    newPos = []
    
    img_out, tform = flag_transform.img_transform(img)
    
    newPos =[ flag_transform.bndbox_transform(bndbox, tform) for bndbox in bndboxs]

    return img_out , newPos

    
def rotation(img, bndboxs):
    newPos = []

    angle =(np.random.randn(1)*8)[0]

    img_out = rotate_transform.img_transform(img, angle)

    rot_center = np.array( (img.size[0]/2 , img.size[1]/2) ) 
    
    newPos = [ rotate_transform.bndbox_transform(bndbox, rot_center, angle) for bndbox in bndboxs]

    return img_out , newPos

def ripple(img, bndboxs):
    newPos = []
                
    img_out, tform = ripple_transform.img_transform(img)
                
    newPos = [ripple_transform.bndbox_transform(bndbox, tform ) for bndbox in bndboxs]
   
    return img_out , newPos


def formbox(pos):
    
    (code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb ) = pos
    oldPos = []
    
    for idx in range(6):
        if idx == 0: # draw the English alphabet 
            oldPos.append((code_x , code_y , code_x + CodeWidth_En, code_y + CodeHeight_En ))
        elif idx == 1: # draw the first number
            oldPos.append((code_x + CodeWidth_En  , code_y , code_x + CodeWidth_En + CodeWidth_Nb, code_y + CodeHeight_Nb ))
        else: # draw the rest numbers
            oldPos.append((code_x + CodeWidth_En + (idx-1)*(CodeWidth_Nb) , code_y , code_x + CodeWidth_En + (idx-1)*(CodeWidth_Nb) + CodeWidth_Nb, code_y + CodeHeight_Nb ))
    return oldPos
    
if __name__ == '__main__':  
    from PIL import Image, ImageDraw
    import cPickle as pickle
    import glob
    import matplotlib.pyplot as plt
    
    q = glob.glob('./data/raw_targets2/raw_targets*.p')
    
    img, code, font_path, code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb = pickle.load( open( np.random.choice(q), "rb" ) )

    pos = (code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb )

    bndboxs = formbox(pos)

    img_out, newPos  =perspective(img, bndboxs)
    img_out, newPos  =flag(img_out, newPos)
    img_out, newPos  =ripple(img_out, newPos)
    img_out, newPos  =rotation(img_out, newPos)

    fig, ax = plt.subplots()

    for pos in newPos:
        (left,top,right,bottom)= pos
    
    
        d = ImageDraw.Draw(img_out)
    
        d.line((left, top, right, top), fill=(255,0,255,255), width=4)
        d.line((right, top, right, bottom), fill=(255,0,255,255), width=4)
        d.line((right, bottom, left, bottom), fill=(255,0,255,255), width=4)
        d.line((left, bottom, left, top), fill=(255,0,255,255), width=4)

    ax.imshow(img_out)

#
#
#    # line transformed
#    label_pos_x = np.hstack( ( np.linspace(100,300,10), np.linspace(100,300,10)))
#    label_pos_y = np.hstack( ( np.linspace(100,100,10), np.linspace(300,300,10)))
#    x, y = np.meshgrid(label_pos_x, label_pos_y) 
#    tline = np.dstack([x.flat, y.flat])[0]
#    plt.plot(tform.inverse(tline)[:, 0], tform.inverse(tline)[:, 1] ,'.b')
#    ax.imshow(out)
