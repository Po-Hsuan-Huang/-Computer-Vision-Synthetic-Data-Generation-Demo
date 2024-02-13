#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 18:10:29 2017

@author: po-hsuan

Edited and annotated on Wedd Mar 15 2017

Wan_Jin_Shi Marathon tag, code recognition project. 

All rights reserved by Acer.Inc

by Po-Hsuan Huang



Description :
    
    The file generates marathon runner's tag cloth on a random background image.
    The runner's registration number and positions of the numbers are randomly generated and labeled in the .xml
    annotation file stored in /Annotations. Alone wiht the .jpg files stored in /JPEGImages the training data set
    then is used to train a CNN to recognize numbers on the tag cloth in a image.
    
Dependencies : 
    This file is never run as main. Call the main function to execute.
    
Optional Features :
    Bounding boxes can be drawn if variable isDraw == True
    Texture, deformation, shades can be manipulated by calling functions
    in modules 'text.py', 'perspective_transform.py', 'shadeLeaves.py',
    'flag_transform.py'
    
    * Flag_transform.py is currently disabled since it is unstable.
    * The file can only generate one tag cloth in a image now.
    
    Updated on March 22 2017
    
    


"""
#import cv2
import os
import math
from PIL import Image, ImageFont, ImageDraw
import numpy as np		
import matplotlib.pyplot as plt
from skimage import util, img_as_float, io
import glob		
from lib.image import shadeLeaves,texture, HSL 
from lib.transform import transform
from Any2VOC_function_many_targets import *
from string import join
import pickle as pickle
import subprocess
import fnmatch
#constats

OVERWRITE = True
SYNC = False

#%%
SyncBatchSize = 0

def get_sync_batch(number):
    global SyncBatchSize 
    if number > 0:
        SyncBatchSize = number
            
def get_overwrite(boolean):
    global OVERWRITE   
    OVERWRITE = boolean

def get_sync(boolean):
    global SYNC
    SYNC = boolean
    
def get_gen_type(train, test):
    global isTrain, isTest 

    isTrain = train
    isTest = test
    

def random_space(min_num,max_num):
    n_space =np.random.randint(min_num,max_num)
    space = ""
    for i in range(n_space) :
       space = space + " "
    return space
#%%   
'''
gen_code() produces an id code that is printed on shipping containers. It consists of a 4-letter English code,
,6 digit-numbers, and tailed by a boxed ckecking number. (i.e., HMCU 232839 A) 
 
In this version the function is modified to produce the id code for the runners in a marathon.
The code consists of an alphabet and 5 digit numbers.(i.e., A 00001)

'''
#E_code_book = {"A": 10, "B": 12, "C": 13, "D": 14, "E": 15, "F": 16, "G": 17, "H": 18, "I": 19, 
#                   "J": 20, "K": 21, "L": 23, "M": 24, "N": 25, "O": 26, "P": 27, "Q": 28, "R": 29, 
#                   "S": 30, "T": 31, "U": 32, "V": 34, "W": 35, "X": 36, "Y": 37, "Z": 38}

#E_code_book='ABCDEFGHIJKLMNOPQRSTUVWXYZ'      

def gen_code():
    
    '''produce english code''' 
    E_code = np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    E_code_book = {"A": 10, "B": 12, "C": 13, "D": 14, "E": 15, "F": 16, "G": 17, "H": 18, "I": 19, 
                   "J": 20, "K": 21, "L": 23, "M": 24, "N": 25, "O": 26, "P": 27, "Q": 28, "R": 29, 
                   "S": 30, "T": 31, "U": 32, "V": 34, "W": 35, "X": 36, "Y": 37, "Z": 38}
    # CATEGORY_INDENTIFIER
#    CI = ['EGHU', 'EGSU', 'EISU', 'EMCU', 'HMCU', 'PCIU', 'DRYU', 'EITU', 'WHLU', 'TCNU', 'IMTU', 'KKFU']
    E_code_book='ABCDEFGHIJKLMNOPQRSTUVWXYZ'      
#    E_weight = [1, 2, 4, 8]
#    N_weight = [16, 32, 64, 128, 256, 512]
    
    
    '''produce english code'''   
    for En_n in range(1): 
#        En = CI[CI_n][En_n]  
#        check_sum = check_sum + E_code_book[En] * E_weight[En_n]
#        E_code = E_code + str(En)
        CI_n = np.random.randint(0,25)
        E_code = E_code_book[CI_n]
        
    '''produce number code'''
    Nu = np.random.randint(0,9,5)
    N_code  = join( [str(i) for i in list(Nu)],sep ='')
    
#    check_sum = check_sum/11.0+0.09
#    check_code = int(np.fix( (check_sum - np.fix(check_sum)) * 10 ))
    return(E_code, N_code)
#%%
colordict={'green':(86, 189, 174),'red':(219, 109, 116),'grey':(139, 138, 138),'violet':(129, 65, 140),'blue':(12, 105, 172),'yellow':(226, 198, 0)}
colorboard=['green', 'red','grey','violet','blue','yellow']
templates = ['01p.png','02p.png','03p.png','04p.png','05p.png','06p.png']

def gen_target_img(img, bndboxs, filename, font_list, bg_list):    
    
    #---Paste shades on template and text----------------------------------------------------------------

#    img = HSL.Hue(img)
    img = HSL.Brightness(img)
    img = HSL.Contrast(img)
    img = HSL.Sharpness(img)
    img =texture.draw_shade(img, 'heavy_crumple')
    img = shadeLeaves.draw_shade(img, 2, Random_Color=True)
     
    img =texture.draw_shade(img, 'spray')
    img =texture.draw_shade(img, 'stain')
    img =texture.draw_shade(img, 'fabric')
    
#%% Transform the image
    img, bndboxs = transform.perspective(img, bndboxs)
    img, bndboxs = transform.ripple(img, bndboxs)
#    img, bndboxs = transform.flag(img, bndboxs)
#    img, bndboxs = transform.rotation(img, bndboxs)


    return img, bndboxs

#%% transform the bounding boxes    
#def gen_bndbox_pos( code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb, coeffs, tform, angle ,rot_center):
#
#    '''
#   
#    code_x, code_y : pos of text
#   
#    CodeWidth_En, CodeHeight_En : Shape of the English alphabet of the text 
#   
#    CodeWidth_Nb, CodeHeight_Nb : Shape of the last 5 digit of the text
#   
#    coeffs :  coefficients for the perspective transformation
#   
#    frequency : frequency of the flag waveform 
#    
#    '''
#
#    oldPos = []
#    newPos_rot = []
#    newPos_pers = [] 
#    newPos = []
#    
#    for idx in range(6): 
#        if idx < 1: # draw the English alphabet 
#            oldPos.append((code_x , code_y , code_x + CodeWidth_En, code_y + CodeHeight_En ))
#            # get bndbox_pos after perspective transform
#            newPos_pers.append( perspective_transform.bndbox_transform(oldPos[idx], coeffs ) )
#            # get bundbox_pos after flag transform  
#            newPos.append( flag_transform.bndbox_transfrom(newPos_pers[idx], tform))
#            # get bndbox_pos after rotational transform
#            newPos_rot.append(rotate_transform.bndbox_transform(newPos[idx], rot_center, angle))
#            
#        elif idx == 1: # draw the first number
#            oldPos.append((code_x + CodeWidth_En  , code_y , code_x + CodeWidth_En + CodeWidth_Nb, code_y + CodeHeight_Nb ))
#                 
#            # get bndbox_pos after perspective transform
#            newPos_pers.append( perspective_transform.bndbox_transform(oldPos[idx], coeffs ) )
#
#            #get bundbox_pos after flag transform  
#            newPos.append( flag_transform.bndbox_transfrom(newPos_pers[idx], tform))
#
#            # get bndbox_pos after rotational transform
#            newPos_rot.append(rotate_transform.bndbox_transform(newPos[idx], rot_center, angle))
#            
#        else: # draw the rest numbers
#            oldPos.append((code_x + CodeWidth_En + (idx-1)*(CodeWidth_Nb) , code_y , code_x + CodeWidth_En + (idx-1)*(CodeWidth_Nb) + CodeWidth_Nb, code_y + CodeHeight_Nb ))
#          
#            # get bndbox_pos after perspective transform
#            newPos_pers.append( perspective_transform.bndbox_transform(oldPos[idx], coeffs ) )
#
#            # get bundbox_pos after flag transform  
#            newPos.append( flag_transform.bndbox_transfrom(newPos_pers[idx], tform))
#
#            # get bndbox_pos after rotational transform
#            newPos_rot.append(rotate_transform.bndbox_transform(newPos[idx], rot_center, angle))
#                    
#    return newPos_rot, newPos_pers

def draw_lottery( prize, people) :
    '''
    parameters
        prize : a list of objects with values
        people : total number of draws 
    return 
        pool : a shuffled list of size poeple
    '''
    pool = np.zeros(people, dtype = int)
    pool[0 : len(prize)] = range(1, len(prize) + 1)
    idx = range(people)
    np.random.shuffle(idx)
    pool = pool[idx]
    return pool, idx

#%% Crop off tansparent part of the image to fit the image in the frame---
def paste_target_on_background(img_list, bg, newPos_list, num_grid):
    '''
    Paste target images on a background. Resized new positions of the bounding
    boxes are also returned. This Posisitons are the fianl positions to be drawn
    on the background image.
    
    
    parameters:
        img_flag : tuple of tager images
            the images to be pasted on the background image
            
        bg : background image
        
        newPos_list : a list of tuples 
            storing the positions of bounding boxes. position needs to be
            resized alone with the target images.
            
        num_grid : int, number of grid 
            used to generate grip map for ranodom pasting. 
            
    return:
        bg : background image after pasting
        
        img_list: list of resized_img
        
        newPos_list : a list of tuples 
            resized positions of text bounding boxes
            
        pastePos_list : a lst of tuples
            posistions of target images
    
    '''
    
    assert len(newPos_list) == len(img_list)
    # resize the images to conform to the background
    # check code bbox padding rate
       
    bbox_padding = 0 
    pastePos_list = [0]*len(img_list)
    pasteSize_list =  [0]*len(img_list)
    # resize img and its newPos to fit the background size

    for i, img in enumerate( img_list):
        newPos = newPos_list[i]
 #       print 'newpos:', newPos
        img_w, img_h = img.size 
        aspect_ratio = float(img_h)/ float(img_w)
    
        bg_w, bg_h = bg.size
            
#        paste_size_w = int(min(bg_w, bg_h) * np.random.uniform(0.1,0.4))
        '''skewed distribution of the image sizes with mean at 0.2'''
        paste_size_w = int(min(bg_w, bg_h) * np.random.gamma(2,0.1))
        paste_size_w = max(min(bg_w, bg_h)*0.05, paste_size_w)
        paste_size_w = min(min(bg_w, bg_h)*0.3 , paste_size_w)
        paste_size_w = int(paste_size_w)
        paste_size_h =  int(paste_size_w * aspect_ratio)

        img = img.resize((paste_size_w, paste_size_h))
        # removing the transparent margin of the img after transformation
        bbox = img.getbbox()
        right = bbox[0]
        top =bbox[1]
        img = img.crop(bbox)
        img_list[i] = img
        
        resize_ratio = float(paste_size_w) / float(img_w)        
        newPos_list[i] = np.array(newPos) * resize_ratio - (right,top,right,top )

        pasteSize_list[i] = (paste_size_w, paste_size_h)
#%% paste SSC to background

    # generate random-sized meshgrid to paste images  
    gridx, step_x = np.linspace(bg_w, 0, num_grid, endpoint = False, retstep = True)
    gridy, step_y = np.linspace(bg_h, 0, num_grid, endpoint = False, retstep = True )
    gridx, gridy = np.meshgrid(gridx, gridy)
    # draw lottery to assign with grid cell contains a target
    pool ,pool_idx = draw_lottery(img_list, len(gridx.flat))

    for j, (grid_w, grid_h) in enumerate(zip(gridx.flat, gridy.flat)):
        #if contain target
        if pool[j] != 0:
            
            paste_size_w, paste_size_h = pasteSize_list[pool_idx[j]]
            allow_w = grid_w - paste_size_w 
            allow_h = grid_h - paste_size_h 
#            print 'grid_x, grid_y, grid_w, grid_h',grid_w + step_x, grid_h + step_y, grid_w, grid_h
#            print 'paste_size_w, paste_size_h', paste_size_w, paste_size_h
         
            paste_x = int(np.fix(np.random.uniform( grid_w + step_x  , allow_w ) ) + 10 )
            paste_y = int(np.fix(np.random.uniform( grid_h + step_y  , allow_h ) ) + 10 )
            paste_x, paste_y = max(0, paste_x), max(0, paste_y)
            
            pastePos_list[pool_idx[j]] = (paste_x, paste_y)
            img = img_list[pool_idx[j]]
            
            bg.paste(img, (paste_x, paste_y), img)
            
            #--------------------------------------------------------------------------
            # Whether to draw bounding boxes on the screen.
            isDraw = False
            
            if isDraw :   
            #---Draw bbox on bg---
                newPos = newPos_list[pool_idx[j]]

                d = ImageDraw.Draw(bg)
            
                bbox_x1 = max( int(paste_x - bbox_padding ), 0)
                bbox_y1 = max( int(paste_y - bbox_padding ), 0)
                bbox_x2 = min( int(paste_x + paste_size_w + bbox_padding), bg_w)
                bbox_y2 = min( int(paste_y + paste_size_h + bbox_padding), bg_h)
                d.line((bbox_x1, bbox_y1, bbox_x1, bbox_y2), fill=(255,255,255,255), width=4)
                d.line((bbox_x1, bbox_y1, bbox_x2, bbox_y1), fill=(255,255,255,255), width=4)
                d.line((bbox_x1, bbox_y2, bbox_x2, bbox_y2), fill=(255,255,255,255), width=4)
                d.line((bbox_x2, bbox_y1, bbox_x2, bbox_y2), fill=(255,255,255,255), width=4)
            
               
                d = ImageDraw.Draw(bg)
                for idx in range(6):
                    alpha = img.split()[-1]
                    real_w, real_h = img.crop(alpha.getbbox()).size

                    #----Draw bounding box on text (after transformation)--------------------------------------------------------------
              
                    bbox_x1 = int(paste_x + newPos[idx][0] - bbox_padding )
                    bbox_y1 = int(paste_y + newPos[idx][1] - bbox_padding )
                    bbox_x2 = int(paste_x + newPos[idx][2] + bbox_padding )
                    bbox_y2 = int(paste_y + newPos[idx][3] + bbox_padding )
                    d.line((bbox_x1, bbox_y1, bbox_x1, bbox_y2), fill=(0,255,0,255), width=4)
                    d.line((bbox_x1, bbox_y1, bbox_x2, bbox_y1), fill=(0,255,0,255), width=4)
                    d.line((bbox_x1, bbox_y2, bbox_x2, bbox_y2), fill=(0,255,0,255), width=4)
                    d.line((bbox_x2, bbox_y1, bbox_x2, bbox_y2), fill=(0,255,0,255), width=4)

#    fig, ax = plt.subplots()
#    
#    plt.imshow(bg)
    
    return pastePos_list, newPos_list, img_list, bg
#%% Create .xml of image---
def create_xml(pastePos_list, img_list, newPos_list, font_path_list, bg, code_list, filename):
    global DATA_PATH, LABEL_PATH, OVERWRITE
    margin = 10 # margin of the boundingbox 
    assert len(pastePos_list) == len(img_list)
    assert len(pastePos_list) == len(newPos_list)
    bg_w, bg_h = bg.size
    num_image = len(img_list)
    img_pos = [0]* num_image
    text_pos = [0]* num_image
    text_space = [0]* num_image
    class_labels = [0]* num_image
    for i in range(num_image):
        paste_x, paste_y = pastePos_list[i]
        newPos = newPos_list[i]
        img = img_list[i]
        font_path = font_path_list[i]
        paste_size_w , paste_size_h = img.size
        #constrain img bbox inside bg 
        img_pos[i] =( max( paste_x - margin, 0),
                      max( paste_y - margin, 0),
                      min( paste_x + paste_size_w + margin , bg_w),
                      min( paste_y + paste_size_h + margin, bg_h)
                      )
        text_pos[i] = list ( np.array(newPos) + np.array((paste_x, paste_y, paste_x, paste_y)))
        text_space[i] = 6
        class_labels[i] = ['tag'] + list(code_list[i])
        
        
    tree = VOCxml( filename +'.jpg', bg, class_labels, img_pos, text_pos, text_space, font_path )    
#    tree.write('./Annotations/TestSet2/'+ filename + ".xml") 
    tree.write( LABEL_PATH + filename + ".xml")
    #--------------------------------------------------------------------------
    
    #---Save image (No noise version)---
    #bg.save('./JPEGImages/'+ filename +'.jpg','JPEG', quality=90)
    #--------------------------------------------------------------------------
    
    #---Save image (with noise)---
    bg = img_as_float(bg)
    mean = np.random.uniform(0, 0.003)
    var = np.random.uniform(0.00001, 0.0005)
    bg = util.random_noise(bg, mode='gaussian', mean=mean, var=var)
    
    
#    io.imsave('./JPEGImages/TestSet2'+ filename +'.jpg', bg,  quality=90)
    io.imsave(DATA_PATH + filename +'.jpg', bg,  quality=90)

    return
#--------------------------------------------------------------------------

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

#----Main code here -------------------------------------------------------------------

def GenData_many_targets(img_num, initial_name, data_path, label_path, text_path):
    global DATA_PATH, LABEL_PATH, SyncBatchSize
    global isTrain, isTest
    global SYNC, OVERWRITE
    
    DATA_PATH = data_path   # path for JPEGImages
    LABEL_PATH = label_path # path for Annotations
    # path for ImageSet
    target_src_path = '/home/pohsuan/Documents/Marathon2017/data/raw_targets2/'

    DATA_PATH = data_path
    LABEL_PATH = label_path
    
    font_list = glob.glob('./font/*.*')
#    bg_list = glob.glob('./background/bg_train_sets/*.jpg')
#    bg_list = glob.glob('./data/background/*.jpg')
    bg_list = []
    for root, dirnames, filenames in os.walk('./background/'):
        for filename in fnmatch.filter(filenames, '*.jpg'):
            bg_list.append(os.path.join(root, filename))    


    # path to the remote folder for synchronizing
    
#    os.remove('/home/acer/Documents/Marathon/' + 'sync.sh')
    sync_data_dst = '/home/pohsuan.huang/pva-faster-rcnn/data/VOCdevkit2007/sycfolder/JPEGImages' 
    sync_label_dst ='/home/pohsuan.huang/pva-faster-rcnn/data/VOCdevkit2007/sycfolder/Annotations'
    with open( '/home/pohsuan/Documents/Marathon2017/' + 'sync.sh',"w") as fo:
        
        fo.writelines(['#!/bin/sh\n', 
                       '# open -u <user> <password> <host url>; mirror -c -R -L <path from> <path to>\n',
                       'lftp -c "open -u pohsuan.huang,acer 10.36.169.170; mirror -c -R -L '
                       + data_path + ' ' + sync_data_dst + '"\n','\n'
                      ])
        fo.writelines(['lftp -c "open -u pohsuan.huang,acer 10.36.169.170; mirror -c -R -L '
                       + label_path + ' ' + sync_label_dst + '"\n'])
    
    os.chmod('sync.sh', 0o775)            
    
    for code_no in range(initial_name + 1, initial_name + img_num + 1):        
        filename = '{:07d}'.format(code_no)
        
        if not os.path.isfile(DATA_PATH + filename +'.jpg') or OVERWRITE:
#        print filename    
            
            if isTrain:  
                with open( text_path + 'trainval.txt',"a") as file:
                    file.write(filename+"\n")
            
            if isTest:             
                with open( text_path + 'test.txt',"a") as file:
                    file.write(filename+"\n")
            
            
            #%%
            num_grid = np.random.randint(2,4) 
            
            max_num_img = math.pow(num_grid, 2)
            # number of targets must be less then number of grid cells
            num_img = np.random.randint(4-1, max_num_img) 
            newPos_list = [0] * num_img
            newPos_pers_list = [0] * num_img
            img_list = [0] * num_img
            pastePos_list = [0] * num_img
            code_list = [0] * num_img
            font_path_list = [0] * num_img
            
            # init variables
#            img, code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb,font_path, code = gen_raw_img(font_list)
            q = glob.glob('./data/raw_targets2/raw_targets*.p')
            for i in range(num_img):
                
                # Generate raw target sets     
                img, code, font_path, code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb = pickle.load( open( np.random.choice(q), "rb" ) )
                
                # Generate  with targets on it.
                
                bndboxs = formbox(( code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb))

                img, newPos = gen_target_img(img,bndboxs ,filename, font_list, bg_list)

                font_path_list[i] = font_path
                img_list[i] = img
                newPos_list[i] = newPos
                code_list[i] = code
                       
            #---Create background for the SCC---
            while True:
                bg_no = np.random.randint(0,len(bg_list))
                try:            
                    bg = Image.open(bg_list[bg_no]).convert("RGBA")
                    break
                except (SyntaxError, IOError):
                     # You can always log it to logger
                    print bg_list[bg_no], ' is bigger than MaxBlock. Retry...'
            
            pastePos_list, newPos_list, img_list, bg = paste_target_on_background(img_list, bg, newPos_list, num_grid)
            create_xml(pastePos_list, img_list, newPos_list, font_path_list, bg, code_list, filename)
            # folder sync fromo local to remote 
            if SYNC:
                if code_no % SyncBatchSize == 0 and SyncBatchSize != 0:
                    subprocess.call('/home/pohsuan/Documents/Marathon2017/' + 'sync.sh')
                    


if __name__ == '__main__':
    import time
    isTrain = True
    isTest = False
    img_num = 10
    initial_name = 10    
# trian annotation data path
    label_path = '/home/pohsuan/disk1/Marathon/Annotations/test/' 
# train_data_output_path
    data_path = '/home/pohsuan/disk1/Marathon/JPEGImages/test/'
# train_data_output_path
    txt_path = '/home/pohsuan/disk1/Marathon/ImageSets/Main/' 
    start = time.clock()
    GenData_many_targets(img_num, initial_name, data_path, label_path, txt_path)
    end = time.clock()
    
    print format('runtime : %.50f' % end-start)

