#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 09:48:41 2017

@author: pohsuan
"""

from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
from skimage import data



sine_amp = 70

image = data.astronaut()
image = Image.open('/home/pohsuan/Documents/Marathon2017/templates/06p.png')
image = np.array(image)

image = np.pad(image, ((sine_amp, sine_amp),(0,0),(0,0)), 'constant', constant_values=((0,0),(0,0),(0,0)))

rows, cols = image.shape[0], image.shape[1]

src_cols = np.linspace(0, cols, 20)
src_rows = np.linspace(0, rows, 10)
src_cols, src_rows = np.meshgrid(src_rows, src_cols) #convention of the meshgrid is transpose 

src = np.dstack([src_rows.flat, src_cols.flat])[0]
# before
plt.figure()
plt.plot(src[:, 0], src[:, 1], '.y')
plt.imshow(image)
label_pos_x = np.hstack( ( np.linspace(100,400,10), np.linspace(100,400,10)))
label_pos_y = np.hstack( ( np.linspace(200,200,10), np.linspace(300,300,10)))
x, y = np.meshgrid(label_pos_x, label_pos_y) 
plt.plot(x,y,'.b')

# add sinusoidal oscillation to row coordinates
sin =  np.sin(np.linspace(0, 2 *np.pi, 20)) * sine_amp
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
out = Image.fromarray(np.uint8(out*255))

fig, ax = plt.subplots()
#ax.imshow(out)

ax.plot(tform.inverse(src)[:, 0], tform.inverse(src)[:, 1], '.c')
#%% bounding lines
label_pos_x = np.hstack( ( np.linspace(100,400,10), np.linspace(100,400,10)))
label_pos_y = np.hstack( ( np.linspace(200,200,10), np.linspace(300,300,10)))

label_rows, label_cols = np.meshgrid(label_pos_x, label_pos_y)
label = np.dstack([label_rows.flat, label_cols.flat])[0]
ax.plot(tform.inverse(label)[:, 0], tform.inverse(label)[:, 1], '.b')

#%% bounding box
row_t = tform.inverse(label)[:, 0]
col_t = tform.inverse(label)[:, 1]
left = min(row_t)
right = max(row_t)
top = min(col_t)
bottom = max(col_t)
ax.imshow(out)

d = ImageDraw.Draw(out)

d.line((left, top, right, top), fill=(255,0,255,255), width=4)
d.line((right, top, right, bottom), fill=(255,0,255,255), width=4)
d.line((right, bottom, left, bottom), fill=(255,0,255,255), width=4)
d.line((left, bottom, left, top), fill=(255,0,255,255), width=4)

ax.imshow(out)






#ax.axis((0, out_cols, out_rows, 0))
ax.axis((-100, 600, 600, -100))

plt.show()