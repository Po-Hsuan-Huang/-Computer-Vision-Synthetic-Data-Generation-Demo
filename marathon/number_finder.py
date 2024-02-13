#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 16:52:49 2017

@author: pohsuan

Draw detected texts on the tag images.

The detected objects are first classified into alphabets and numbers.

Only the alphabet with the highest confidence is kept.

The numbers are first trimed with IoU(Intersectoin of Union) and NMS
(Non-Maximum Suppress), where the confidence of boundingboxes with large
 overlaps are compared. Only the one with the higher confidence is kept.
 
 
Threshold of detection and threshold of IoU can be reset to perferable values
(default value 0.5 and 0.5) 

***
The mis-classification between alphabets and numbers are not handled, so confusion
between, say, '3' and 'B', '4' and 'A', 'D' and '0', can occur.  

It is assumed the correct text begins with an alphabet tailed with 5 numbers.
***

"""




from PIL import Image, ImageFont, ImageDraw
import pickle, os, cv2, glob
import numpy as np
from pylab import *



def IOU(a,b):
    '''
    calcualte the intersetion of union of two bounding boxes a,b.
    a,b are four-tuple position
    '''
    #intersection
    x1,y1,x2,y2 = a
    x3,y3,x4,y4 = b
    
    x5 = max(x1,x3)
    y5 = max(y1,y3)
    x6 = min(x2,x4)
    y6 = min(y2,y4)
    
    I = ( x6- x5 )*(y6 - y5 ) # intersection

    U = ( x2- x1 )*(y2 - y1 ) + ( x4- x3 )*(y4 - y3 ) - I # union
    
    return I/U

def NMS(seq):
    '''
    Take a sequence of bounding boxes sorted by x pos,
    
    and suppress regions with lower confidence
    
    when IOU is higher than the threshold 
    '''
    # sort the order of x pos
    sort_x = np.array( sorted( (obj['pos'][0], i) for i, obj in enumerate(seq)))
    pos_seq = [ seq[idx] for idx in sort_x[:,1] ]
    
    # sort pos_seq by x pos
    iou_thres = 0.5
    n = 0
    while n < len(pos_seq)-1:
        print n, len(pos_seq)
        if IOU(pos_seq[n]['pos'], pos_seq[n+1]['pos']) >= iou_thres:
           # compare conf
            print 'ha'
            if pos_seq[n]['conf'] >= pos_seq[n+1]['conf']:
                pos_seq.pop(n+1)  
            else :
                pos_seq.pop(n)
        else:
            n += 1


    return pos_seq
           
                  
step2 = True
if step2 :   
    # for phon2016step2
    pkl_path = '/home/pohsuan/Documents/Marathon2017/detections/detects-phone2016-step2/'
    txt_path = '/home/pohsuan/Documents/Marathon2017/detections/detects-phone2016-step2/'
    img_path = '/home/pohsuan/Documents/Marathon2017/tag_pics/realpho2016phone/'
    bg_img_path = '/home/pohsuan/Documents/Marathon2017/detections/detects-phone2016/'
    dest_path = '/home/pohsuan/Documents/Marathon2017/detections/detects-phone2016-step2/' 
with open(txt_path +'test.txt') as f:
    data = f.readlines()
with open(pkl_path + 'detections.pkl', 'rb') as f1:
    imgbox = pickle.load(f1)
    
if not os.path.exists(dest_path + '/output/'):
    os.makedirs( dest_path + '/output/')      
    
    
clsnum=38
cls_name=[
        '__background__', # always index 0
        'tag','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
        'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
        'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']



#%% Darw text on tag images

images  = sorted(glob.glob( img_path+ "*.jpg" ) )

for i, img in enumerate(images):
    print('%d/%d'%(i,len(images)))
    imgname=data[i]
    kk=imgname[:imgname.find("\n")]
    jpgname='%s.jpg'%(kk)
    img = Image.open(img)
    detections =[]
    for k in range(0,clsnum):
        if len(imgbox[k][i])>0:
            for j in range(0,len(imgbox[k][i])):
                x1=int(imgbox[k][i][j][0])
                y1=int(imgbox[k][i][j][1])
                x2=int(imgbox[k][i][j][2])
                y2=int(imgbox[k][i][j][3])
                conf=imgbox[k][i][j][4]
                if conf>0.5: # confince value 
                    font=cv2.FONT_HERSHEY_SIMPLEX                   
                    conf2=str(round(float(conf),3))
                    text='%s(%s)'%(cls_name[k],conf2)
                    print(text)
                    detections.append({'text': cls_name[k],'pos': (x1, y1, x2, y2), 'conf': conf})

    
    # sort away the alphabet with lower conf
    alps = [obj for obj in detections if obj['text'] in  ['a','b','c','d']]
    if alps != []:
        sort_idx = sorted((obj['conf'], i) for i, obj in enumerate(alps))[0][1]
        alp = [alps[sort_idx]['text']]
    else:
        alp = []
       
    nums = [obj for obj in detections if obj['text'] in  list('0123456789')]
    if nums != []:
        num = NMS(nums)
    else:
        num = []
               
    if len(num) > 5:
        num = [obj['text'] for obj in num[:5]]
        
    elif len(num) > 0:
        num = [obj['text'] for obj in num]
    else:
        num=[]
        
    text = ''.join(alp + num).upper()
    colordict={'green':(0, 255, 174),'red':(219, 109, 116),'grey':(139, 138, 138),'violet':(129, 65, 140),'blue':(12, 105, 172),'yellow':(226, 198, 0)}
    fontcolor = colordict['green']
    fontsize  = img.size[0]/5
    font_path = glob.glob('./font/*.*')[0]
    font = ImageFont.truetype(font_path, fontsize)
    d = ImageDraw.Draw(img)
    x,y = img.size    
    d.text( (30,30), text, fontcolor, font=font)    

    img.save( dest_path + '/output/'+  jpgname) 
  