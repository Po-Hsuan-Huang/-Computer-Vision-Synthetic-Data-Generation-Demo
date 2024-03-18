#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:46:51 2017

@author: lab


Generate raw target images and pickle them in format {raw_target_%f}.p.

"""

import os, sys, time
 # Get the directory containing the script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Add the script directory to the Python path
sys.path.append(script_dir)

os.chdir(os.path.dirname(os.path.realpath(__file__)))

cwd = os.getcwd()
sys.path.extend([os.path.join(cwd, "lib/image"), os.path.join(cwd, "lib/transform/util")])
import matplotlib.pyplot as plt
from multiprocessing import Process, cpu_count, JoinableQueue
import math
from PIL import Image, ImageFont, ImageDraw
import numpy as np		
from skimage import util, img_as_float, io
import glob		
import shadeLeaves, texture, flag_transform, perspective_transform	
from Any2VOC_function_many_targets import *
import pickle as pickle


def gen_code():
    
    '''produce english code''' 
#    E_code = np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    E_code = np.random.choice(list('ABCD'))

    '''produce number code'''
    Nu = np.random.randint(0,10,5)
#    Nu =np.random.choice(list('ABCD'), size=5)
    N_code  = "  ".join( [str(i) for i in list(Nu)])
    
    return(E_code, N_code)
#%%
colordict={'green':(86, 189, 174),'red':(219, 109, 116),'grey':(139, 138, 138),'violet':(129, 65, 140),'blue':(12, 105, 172),'yellow':(226, 198, 0)}
colorboard=['green', 'red','grey','violet','blue','yellow']
templates = ['01p.png','02p.png','03p.png','04p.png','05p.png','06p.png']

def gen_raw_img(font_list):
    global colordict, colorboard, templates
    
    sample = np.random.choice(colorboard)
    fontcolor = colordict[sample]
    fontsize  = 80 # np.random.randint(80,120)
    # padding rate for setting the image size of font
    fimg_padding = 1.1
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
    l, t, r, b = font.getbbox(code)
    # Use the draw object to measure the text size
    code_w, code_h = abs(l-r), abs(t-b)
    
    #--------------------------------------------------------------------------
    
    #---Setting the image size of font---
    img_size_w = int((code_w) * fimg_padding)
    img_size_h = int(img_size_w * 0.8)
    #--------------------------------------------------------------------------
    
    
    #---Open runner id template-----------------------------------------------
    # randomely choose one of the 6 templates.
    filepath = os.path.join(cwd , 'templates', str(templates[colorboard.index(sample)])) 
    img = Image.open(filepath)
    img = img.resize((img_size_w, img_size_h))


    d = ImageDraw.Draw(img)
    
    # font size of C_code 
    l, t, r, b= d.textbbox((0,0),C_code, font= font)
    CodeWidth_En, CodeHeight_En = abs(l-r), abs(t-b)

    l, t, r, b= d.textbbox((0,0),N_code, font= font)
    CodeWidth_Nb, CodeHeight_Nb = abs(l-r), abs(t-b)
    CodeWidth_Nb = CodeWidth_Nb/5
    
    code_x = (img_size_w-code_w)/2  
    code_y = (img_size_h-code_h)/2 
    ''' height of the colorband'''
    colorband_h = code_y*0.7
    
    #---Draw rectangle behind the text --
    d.rectangle((0,colorband_h,img_size_w,img_size_h-colorband_h), fill=(255,255,255,255)) # half opaque background under the code
    #---Draw text code on rectangle ---
    d.text( ( code_x, code_y ),code, fontcolor,font=font)    
    
    
    return img, code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb,font_path, code 


def work(font_list, n, k):
        global start
        
        for i in range(n):
        
            j  = n*k + i + 1
            
            img, code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb,font_path, code = gen_raw_img(font_list)
         
            filename = '{:05d}'.format(j)
            
            pickle.dump( [img ,code, font_path, code_x ,code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb], open( dst_path + "raw_targets_" + filename +".p", "wb" ) )
    
#            print 'filename ', filename
            
        end = time.time()   
            
        print(('time: ', end-start))
           

class Worker(Process):          
    
      def __init__(self, queue):
          Process.__init__(self)
          self.queue=queue
          
      def run(self):
          np.random.seed()
          
          while True:
              job=self.queue.get()
              if not job:
                  print(('Exiting...', self.name))
                  print(('Job, ', job))
                  self.queue.task_done()
                  break
              
              else :
#                  print 'working... ',job[0]
                  
                  img, code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb,font_path, code = gen_raw_img(job[1])
                 
                  filename = '{:05d}'.format(job[0])
                    
                  pickle.dump( [img ,code, font_path, code_x ,code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb], open( job[2] + "raw_targets_" + filename +".p", "wb" ) )

                  self.queue.task_done()              
          
          
if __name__ == '__main__':

    
    #%% Main Function
    SingleProcess = True
    
    if SingleProcess:  
        start = time.time()
        cwd = os.getcwd() 
        dst_path = os.path.join(cwd,'Marathon2017/data/raw_targets2/' )
        if not os.path.isdir(dst_path):
            os.makedirs(dst_path)
        font_list = glob.glob(os.path.join(cwd,'font/*.otf'))
        init_num = 0
        
        for i in range(10):
            j = init_num + i + 1
            
            img, code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb,font_path, code = gen_raw_img(font_list)
            fig, ax = plt.subplots()
            ax.imshow(img)
            plt.show()  
            filename = '{:05d}'.format(j)
    #        print 'filename ', filename
            pickle.dump( [img, code, font_path, code_x, code_y, CodeWidth_En, CodeHeight_En, CodeWidth_Nb, CodeHeight_Nb], open( dst_path + "raw_targets_" + filename +".p", "wb" ) )
    
        end = time.time()
        
        print(('time: ', end-start))
    #%% Main Function Multiprocessing
    if not SingleProcess:
        print('Multiprocess...')
            
        start = time.time()
        job_queue = JoinableQueue()
            
        start = time.time()
        cwd = os.getcwd() 
        dst_path = os.path.join(cwd,'Marathon2017/data/raw_targets2/' )
        if not os.path.isdir(dst_path):
            os.mkdir(dst_path)
        font_list = glob.glob(os.path.join(cwd,'font/*.*'))

        process_list = []
    
        num= 50000
        init_num = 0
        
        for i in range(init_num, init_num + num):
            job_queue.put((i,font_list, dst_path))
           
        for p in range(2*cpu_count()-1): # PROCESS_NUM
             job_queue.put(None)
             process = Worker(job_queue)
             process_list.append(process)  
             process.start()
        
        for p in process_list : p.join()
        
        job_queue.join()
        end = time.time()   
    
        print(('time: ', end-start))  
    
    
            
        
