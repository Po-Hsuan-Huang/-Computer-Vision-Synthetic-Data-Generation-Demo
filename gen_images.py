# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 13:47:01 2016

@author: gene
"""

# -*- coding: utf-8 -*-
"""
Edited and annotated on Wedd Mar 15 2017

Wan_Jin_Shi Marathon tag, code recognition project. 

All rights reserved by lab.Inc

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
from PIL import Image, ImageFont, ImageDraw, ImageOps
import numpy as np		
import matplotlib.pyplot as plt		
from skimage import util
from skimage import data, img_as_float, io, color
import sys, glob		
import shadeLeaves, texture, flag_transform, perspective_transform	
from Any2VOC_function import *

 
def random_space(min_num,max_num):
    n_space =np.random.randint(min_num,max_num)
    space = ""
    for i in range(n_space) :
       space = space + " "
    return space
    
'''
gen_code() produces an id code that is printed on shipping containers. It consists of a 4-letter English code,
,6 digit-numbers, and tailed by a boxed ckecking number. (i.e., HMCU 232839 A) 
 
In this version the function is modified to produce the id code for the runners in a marathon.
The code consists of an alphabet and 5 digit numbers.(i.e., A 00001)

'''
def gen_code():
    E_code = ""
    N_code = ""
#    check_sum=0

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
    for Nu_n in range(5): # How many digit in Number
        Nu =  np.random.randint(0,9)
#        check_sum = check_sum + Nu * N_weight[Nu_n]
        N_code = N_code + str(Nu)
    
#    check_sum = check_sum/11.0+0.09
#    check_code = int(np.fix( (check_sum - np.fix(check_sum)) * 10 ))
    return(E_code, N_code)
    


def gen_img(filename, font_list, bg_list):
    # Shipping Cantanter Code = SCC
    
    colordict={'green':(86, 189, 174),'red':(219, 109, 116),'grey':(139, 138, 138),'violet':(129, 65, 140),'blue':(12, 105, 172),'yellow':(226, 198, 0)}
    colorboard=['green', 'red','grey','violet','blue','yellow']
    opaque = np.random.randint(25,221)
    sample = np.random.choice(colorboard)
    fontcolor = colordict[sample]
    fontsize  = np.random.randint(80,120)
    # padding rate for setting the image size of font
    fimg_padding = 1.1
    # check code bbox padding rate
    bbox_gap = 2 # fontsize * 0.05
    
#--------------------------------------------------------------------------
    #---Generate the Shipping Cantanter Code---
    C_code, N_code = gen_code()
    #--------------------------------------------------------------------------
    
    #---Add space between cdoes---
    code = C_code + N_code 
    #--------------------------------------------------------------------------
    
    #---Choice a font type for output---
#    font_no = int(np.fix(np.random.random()*10))
#    font_path = font_list[font_no]
    font_path = font_list[0]

    font = ImageFont.truetype(font_path, fontsize)

    #--------------------------------------------------------------------------
    
    #---Get the related info of font. 
    '''code_w and code_h are objects not variable.'''
    code_w, code_h = font.getsize(code)
    
    #--------------------------------------------------------------------------
    
    #---Setting the image size of font---
    img_size_w = int((code_w) * fimg_padding)
    img_size_h = int(img_size_w * 0.8)
    #--------------------------------------------------------------------------

    
    #---Open runner id template-----------------------------------------------
    # randomely choose one of the 6 templates.
    templates = ['01p.png','02p.png','03p.png','04p.png','05p.png','06p.png']
    filepath = './templates/' + templates[colorboard.index(sample)] 
    img = Image.open(filepath)
    img = img.resize((img_size_w, img_size_h))


    d = ImageDraw.Draw(img)
    
    # font size of C_code 
    CodeWidth_En, CodeHeight_En = d.textsize(C_code,font)
    CodeWidth_Nb, CodeHeight_Nb = d.textsize(N_code,font)
    CodeWidth_Nb = CodeWidth_Nb/5
    
    code_x = (img_size_w-code_w)/2  
    code_y = (img_size_h-code_h)/2 
    ''' height of the colorband'''
    colorband_h = code_y*0.7
    
    #---Draw rectangle behind the text --
    d.rectangle((0,colorband_h,img_size_w,img_size_h-colorband_h), fill=(255,255,255,255)) # half opaque background under the code

    
    #---Draw text code on rectangle ---
    d.text( ( code_x, code_y ),code, fontcolor,font=font)
    #---Paste shades on template and text----------------------------------------------------------------

    img = shadeLeaves.draw_shade(img, 2)
    img =texture.draw_shade(img, 'heavy_crumple')
#    img =texture.draw_shade(img, 'spray')
#    img =texture.draw_shade(img, 'stain')
    img =texture.draw_shade(img, 'fabric')
    
    
    
    
#%%    
    # perspective transform
    img_pers, coeffs, pos = perspective_transform.img_transform(img) 

    img_flag = img_pers
#    img_flag, frequency = flag_transform.transfrom(img_pers)

    # position of text bounding box
    padding = 30
#    oldPos = (code_x-padding, code_y-padding, code_x+padding + code_w, code_y+padding + code_h)
    oldPos = []
    newPos_pers = [] 
    newPos = []
    
    
    for idx in range(6): 
        
        if idx < 1: # draw the En 
            oldPos.append((code_x , code_y , code_x + CodeWidth_En, code_y + CodeHeight_En ))
            
            # get bndbox_pos after perspective transform
            newPos_pers.append( perspective_transform.bndbox_transform(oldPos[idx], coeffs ) )

            # get bundbox_pos after flag transform  
#            newPos.append( flag_transform.bndbox_transfrom( frequency, newPos_pers[idx], img_pers))
             
        elif idx == 1:
            oldPos.append((code_x + CodeWidth_En  , code_y , code_x + CodeWidth_En + CodeWidth_Nb, code_y + CodeHeight_Nb ))
            
            # get bndbox_pos after perspective transform
            newPos_pers.append( perspective_transform.bndbox_transform(oldPos[idx], coeffs ) )

            #get bundbox_pos after flag transform  
#            newPos.append( flag_transform.bndbox_transfrom( frequency, newPos_pers[idx], img_pers))
    
        else:
            oldPos.append((code_x + CodeWidth_En + (idx-1)*(CodeWidth_Nb) , code_y , code_x + CodeWidth_En + (idx-1)*(CodeWidth_Nb) + CodeWidth_Nb, code_y + CodeHeight_Nb ))
            
            # get bndbox_pos after perspective transform
            newPos_pers.append( perspective_transform.bndbox_transform(oldPos[idx], coeffs ) )

            # get bundbox_pos after flag transform  
#            newPos.append( flag_transform.bndbox_transfrom( frequency, newPos_pers[idx], img_pers))

        newPos = newPos_pers
#%% Crop off tansparent part of the image to fit the image in the frame---

    img_w, img_h = img_flag.size 
    aspect_ratio = float(img_h)/ float(img_w)
    #--------------------------------------------------------------------------
    
    #---Add background for the SCC---
    bg_no = np.random.randint(0,len(bg_list))
    bg = Image.open(bg_list[bg_no]).convert("RGBA")
    bg_w, bg_h = bg.size
    
    # resize the SCC image for background

    paste_size_w = int(min(bg_w, bg_h) * np.random.uniform(0.2,0.4))
    paste_size_h =  int(paste_size_w * aspect_ratio)
    

    
    resize_ratio = float(paste_size_w) / float(img_w)
    
    newPos = np.array(newPos) * resize_ratio 

    
    img = img_flag.resize((paste_size_w, paste_size_h))
    # paste SSC to background
    allow_w = bg_w - paste_size_w - 20
    allow_h = bg_h - paste_size_h - 20 
    paste_x = int(np.fix(np.random.uniform( 0 , allow_w ) ) + 10 )
    paste_y = int(np.fix(np.random.uniform( 0 , allow_h ) ) + 10 )
    bg.paste(img, (paste_x, paste_y), img)
    #--------------------------------------------------------------------------
    # Whether to draw bounding boxes on the screen.
    isDraw = False
    if isDraw :   
    #---Draw bbox on bg---
    
        d = ImageDraw.Draw(bg)
    
        bbox_x1 = int(paste_x - bbox_gap )
        bbox_y1 = int(paste_y - bbox_gap )
        bbox_x2 = int(paste_x + paste_size_w + bbox_gap)
        bbox_y2 = int(paste_y + paste_size_h + bbox_gap)
        d.line((bbox_x1, bbox_y1, bbox_x1, bbox_y2), fill=(255,255,255,255), width=4)
        d.line((bbox_x1, bbox_y1, bbox_x2, bbox_y1), fill=(255,255,255,255), width=4)
        d.line((bbox_x1, bbox_y2, bbox_x2, bbox_y2), fill=(255,255,255,255), width=4)
        d.line((bbox_x2, bbox_y1, bbox_x2, bbox_y2), fill=(255,255,255,255), width=4)
    
        #----Draw bounding box on text (after perspective_transformation)--------------------------------------------------------------
       
        d = ImageDraw.Draw(bg)
        for idx in range(6):
#            alpha = img.split()[-1]
#            real_w, real_h = img.crop(alpha.getbbox()).size
#            bbox_x1 = int(paste_x + newPos_pers[idx][0] - bbox_gap )
#            bbox_y1 = int(paste_y + newPos_pers[idx][1] - bbox_gap )
#            bbox_x2 = int(paste_x + newPos_pers[idx][2] + bbox_gap)
#            bbox_y2 = int(paste_y + newPos_pers[idx][3] + bbox_gap)
#            d.line((bbox_x1, bbox_y1, bbox_x1, bbox_y2), fill=(255,0,0,255), width=4)
#            d.line((bbox_x1, bbox_y1, bbox_x2, bbox_y1), fill=(255,0,0,255), width=4)
#            d.line((bbox_x1, bbox_y2, bbox_x2, bbox_y2), fill=(255,0,0,255), width=4)
#            d.line((bbox_x2, bbox_y1, bbox_x2, bbox_y2), fill=(255,0,0,255), width=4)
            
            #----Draw bounding box on text (after flag_transformation)--------------------------------------------------------------
      
            bbox_x1 = int(paste_x + newPos[idx][0] - bbox_gap )
            bbox_y1 = int(paste_y + newPos[idx][1] - bbox_gap )
            bbox_x2 = int(paste_x + newPos[idx][2] + bbox_gap)
            bbox_y2 = int(paste_y + newPos[idx][3] + bbox_gap)
            d.line((bbox_x1, bbox_y1, bbox_x1, bbox_y2), fill=(0,255,0,255), width=4)
            d.line((bbox_x1, bbox_y1, bbox_x2, bbox_y1), fill=(0,255,0,255), width=4)
            d.line((bbox_x1, bbox_y2, bbox_x2, bbox_y2), fill=(0,255,0,255), width=4)
            d.line((bbox_x2, bbox_y1, bbox_x2, bbox_y2), fill=(0,255,0,255), width=4)
#%% Create .xml of image---
    img_pos =(paste_x, paste_y, paste_x + paste_size_w, paste_y + paste_size_h)
    text_pos = list ( np.array(newPos) + np.array((paste_x, paste_y, paste_x, paste_y)))
    text_space = 6
    class_labels = ['tag'] + list(C_code) +list(N_code)
    print(class_labels)
    tree = VOCxml( filename +'.jpg', bg, class_labels, img_pos, text_pos, text_space, font_path )    
    tree.write('./Annotations/'+ filename + ".xml") 
    #--------------------------------------------------------------------------
    
    #---Save image (No noise version)---
    #bg.save('./JPEGImages/'+ filename +'.jpg','JPEG', quality=90)
    #--------------------------------------------------------------------------
    
    #---Save image (with noise)---
    bg = img_as_float(bg)
    mean = np.random.uniform(0, 0.003)
    var = np.random.uniform(0.00001, 0.0005)
    bg = util.random_noise(bg, mode='gaussian', mean=mean, var=var)
    io.imsave('./JPEGImages/'+ filename +'.jpg', bg,  quality=90)
#--------------------------------------------------------------------------


def give_me_SCC_images(img_num):
    
    font_list = glob.glob('./font/*.*')
#    bg_list = glob.glob('./background/bg_train_sets/*.jpg')
    bg_list = glob.glob('./background/bg_train_people/*.jpg')
    bg_list = bg_list
    if os.path.isfile('./trainval.txt'):
        os.remove("./trainval.txt")
    
    for code_no in range(1, img_num+1):
        
        filename = '{:07d}'.format(code_no)
    
        print(filename)    
        
        with open("./trainval.txt","a") as file:
            file.write(filename+"\n")
                    
        with open("./test.txt","a") as file:
            file.write(filename+"\n")
            
        gen_img(filename, font_list, bg_list)



