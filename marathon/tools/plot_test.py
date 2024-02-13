# -*- coding: utf-8 -*-
"""
Created on Wed Apr 05 09:36:56 2017

@author: 1609070
"""


#####將test結果畫出#####
import pickle, os, cv2, glob
import numpy as np
from pylab import *
step2 = False
step1 = True
if step1 : 
    # for phone2016
    pkl_path = '/home/pohsuan/Documents/Marathon2017/detections/detects-phone2016/'
    txt_path = pkl_path
    img_path = pkl_path
    dest_path =pkl_path
elif step2 :   
    # for phon2016step2
    pkl_path = '/home/pohsuan/Documents/Marathon2017/detections/detects-phone2016-step2/'
    txt_path = '/home/pohsuan/Documents/Marathon2017/detections/detects-phone2016-step2/'
    img_path = '/home/pohsuan/Documents/Marathon2017/tag_pics/realpho2016phone/'
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

images  = sorted(glob.glob( img_path+ "*.jpg" ) )

#%%    
for i, img in enumerate(images):
    print('%d/%d'%(i,len(images)))
    imgname=data[i]
    kk=imgname[:imgname.find("\n")]
    jpgname='%s.jpg'%(kk)
    img = cv2.imread( img)
        
    for k in range(0,clsnum):
        if len(imgbox[k][i])>0:
            for j in range(0,len(imgbox[k][i])):
                x1=int(imgbox[k][i][j][0])
                y1=int(imgbox[k][i][j][1])
                x2=int(imgbox[k][i][j][2])
                y2=int(imgbox[k][i][j][3])
                conf=imgbox[k][i][j][4]
                if conf>0.4: # confince value 
                   
                    if k==1:
                        if np.any([cls_name[k]==p for p in ['a','b','c','d']]):
                            color = (0,255,0)
                        elif np.any([cls_name[k]==p for p in list('1234567890')]):
                            color = (255,255,0)                                            
                        else : 
                            color = (255, 0, 0)
                        cv2.rectangle(img,(x1,y1), (x2,y2), color,3)
                        font=cv2.FONT_HERSHEY_SIMPLEX                   
                        conf2=str(round(float(conf),3))
                        text='%s(%s)'%(cls_name[k],conf2)
                        print(text)

                        cv2.putText(img,text,(x1,y1-10),font,0.3,color,1)
                        
                    if 2 <= k <= 27:
                        if np.any([cls_name[k]==p for p in ['a','b','c','d']]):
                            color = (0, 255,0)
                        elif np.any([cls_name[k]==p for p in list('1234567890')]):
                            color = (255,255,0)                                            
                        else : 
                            color = (255, 0, 0)
                        cv2.rectangle(img,(x1,y1), (x2,y2), color,3)
                        font=cv2.FONT_HERSHEY_SIMPLEX                   
                        conf2=str(round(float(conf),3))
                        text='%s(%s)'%(cls_name[k],conf2)
                        print(text)
                        cv2.putText(img,text,(x1,y1-10),font,0.3,color,1)
                    if 28 <= k :
                        if np.any([cls_name[k]==p for p in ['a','b','c','d']]):
                            color = (0, 255,0)
                        elif np.any([cls_name[k]==p for p in list('1234567890')]):
                            color = (255,255,0)                                            
                        else : 
                            color = (255, 0, 0)
                        cv2.rectangle(img,(x1,y1), (x2,y2), color,3)
                        font=cv2.FONT_HERSHEY_SIMPLEX                   
                        conf2=str(round(float(conf),3))
                        text='%s(%s)'%(cls_name[k],conf2)
                        print(text)

                        cv2.putText(img,text,(x1,y1-10),font,0.3,color,1)
    
               
    cv2.imwrite( dest_path + '/output/'+  jpgname,img) 
