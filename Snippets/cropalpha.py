#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 18:23:34 2017

@author: pohsuanh
"""




from PIL import Image, ImageFont, ImageDraw
import numpy as np		
import matplotlib.pyplot as plt
from skimage import util, img_as_float, io
import glob		
import shadeLeaves, texture, flag_transform, perspective_transform	
from Any2VOC_function_many_targets import *
from string import join
import pickle as pickle
import time

target_src_path = '/home/pohsuanh/Documents/Marathon2017/data/raw_targets/'
q = glob.glob('./data/raw_targets/raw_targets*.p')
img, code, font_path, code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb = pickle.load( open( np.random.choice(q), "rb" ) )
img =texture.draw_shade(img, 'heavy_crumple')
img =texture.draw_shade(img, 'fabric')
#%% Transform the image
# perspective transform
img_pers, coeffs, pos = perspective_transform.img_transform(img) 
img_flag, tform = flag_transform.transfrom(img_pers)
start = time.time()
img_alpha = img_flag.split()[-1]
img_alpha = np.asarray(img_alpha)
rows, cols = img_alpha.shape
# search the first colomn and row with pixel alpha == 255
#print np.min(img_alpha), np.max(img_alpha)

# Search for left
loc1=()
x, y = np.meshgrid(list(range(rows)), list(range(cols)))
for row, col in zip( x.flat , y.flat):
#    print (row, col)
    if img_alpha[row,col] ==255:
        print('find')
        loc1 = (row, col)
        break

left = loc1[1]

# Search for top
loc2=()    
for row, col in zip( x.T.flat , y.T.flat):
#    print (row, col)
    if img_alpha[row,col] ==255:
        print('find')
        loc2 = (row, col)
        break 

top = loc2[0]

# search right
loc1 = ()
x, y = np.meshgrid(list(range(rows)), list(range(cols)))
for row, col in zip( np.fliplr([np.asarray(x.flat)])[0] ,
                    np.fliplr([np.asarray(y.flat)])[0]):
#    print (row, col)
    if img_alpha[row,col] ==255:
        print('find')
        loc1 = (row, col)
        break
right = loc1[1]
# search bottom
loc2 = ()
x, y = np.meshgrid(list(range(rows)), list(range(cols)))
for row, col in zip( np.fliplr([np.asarray(x.T.flat)])[0] ,
                    np.fliplr([np.asarray(y.T.flat)])[0]):
#    print (row, col)
    if img_alpha[row,col] ==255:
        print('find')
        loc2 = (row, col)
        break
    
bottom =loc2[0]

end = time.time()

print(('self_crop_time, ', end-start))
#%%
start = time.time()
box = img_flag.getbbox()
end =time.time()
print(('PIL crop time, ', end-start))
img_crop = img_flag.crop(box)



#%%
fig, ax = plt.subplots()
ax.imshow(img_alpha)

fig, ax = plt.subplots()       
ax.imshow(img_alpha[top:bottom,left:right])

img_crop.show()
#ax.plot(label_pos[0], label_pos[1],'r*')

