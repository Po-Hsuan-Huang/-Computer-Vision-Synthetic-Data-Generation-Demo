#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 16:42:38 2017

@author: pohsuanh
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 11:05:02 2016

@author: pohsuanh & Gene
"""
#
#from gen_images import *
#
#give_me_SCC_images(10)


'''
This file is the main file of Marathon2017. It generates Images and Labels 
that annotates the images. The generated
images and labels can be inspected with GUI labelImage.py 

https://github.com/tzutalin/labelImg

Specify the folders where you wish to store the data.
If not exist yet, the program create a new folder for you.

Specify the size of training set and test set, and the naming follows the 
order that can be used by pva-fast-rcnn.

https://github.com/sanghoon/pva-faster-rcnn

training set : 1 ~ trainset_size

test set : trainset_size + 1 ~ trainset_size + testset_size 


'''
import time
from multiprocessing import Process, cpu_count, JoinableQueue
from gen_images_many_targets import GenData_many_targets, get_gen_type, get_sync_batch, get_overwrite, get_sync
import os, glob, sys
import numpy as np



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
                  print(('working... ',job[0]))
                  GenData_many_targets(1,job[0], job[1], job[2], job[3])
                  self.queue.task_done()              
          
          
if __name__ == '__main__':

    # Get the directory containing the script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Add the script directory to the Python path
    sys.path.append(script_dir)

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    cwd = os.getcwd()

    global start
    
    Gen_train_data = True
    Gen_test_data = False
    SingleProcess = False
    Overwrite = True
    SYNC = False
    # number of training data 
    
    train_num = 500
    
    # number of testing data
    
    test_num = 1
    
    # batchsize sync to remote
    
    SycBatchSize = 20
    
    # initial name for training
    Initial_name_train = 0
    
    # initial name for testing
    Initial_name_test = train_num
        
    get_overwrite(Overwrite)
        
    get_gen_type(Gen_train_data, Gen_test_data)
    
    get_sync_batch(SycBatchSize)
    
    ''' The folders must be created beforehand, remember not to overwrite'''
    
    # trian annotation data path
    train_label_path = os.path.join( cwd, 'Marathon2017/Annotations/TrainSet2/')
    # test annotation data path
    test_label_path = os.path.join(cwd,'Marathon2017/Annotations/TestSet2/') 
    # train_data_output_path
    train_data_path = os.path.join(cwd,'Marathon2017/JPEGImages/TrainSet2/')
    # test_data_output_path
    test_data_path =  os.path.join(cwd,'Marathon2017/JPEGImages/TestSet2/')
    
    # index file tracking whom should be trained and whom should be tested
    text_data_path = os.path.join(cwd, 'Marathon2017/ImageSets/Main/2/') 
    
    ''' Check if the folders exist && empty. If not, create a new folder.'''
    if Gen_train_data :
        print('Gen_train_data')
    
        if os.path.isdir(train_data_path):
            if len(glob.glob(train_data_path +"*.jpg")) != 0 :
                 anw = input( 'TrainData Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
                 if anw.lower() != "y":
                     sys.exit()
        else:
            os.makedirs(train_data_path)
            
        if os.path.isdir(train_label_path):
            if len(glob.glob(train_label_path +"*.xml")) != 0 :
                 anw = input( 'TrainLabel Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
                 if anw.lower() != "y":
                     sys.exit()
        else:
            os.makedirs(train_label_path)
    
    if Gen_test_data:
        print('Gen_test_data')
        
        if os.path.isdir(test_data_path):
            if len(glob.glob(test_data_path +"*.jpg")) != 0 :
                 anw = input( 'TestData Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
                 if anw.lower() != "y":
                     sys.exit()
        else:
            os.makedirs(test_data_path)
        
        
        
        if os.path.isdir(test_label_path):
            if len(glob.glob(test_label_path +"*.xml")) != 0 :
                 anw =input( 'TestLabel Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
                 if anw.lower() != "y":
                     sys.exit()
        else:
            os.makedirs(test_label_path)
    
    '''Check text_path''' 
    if os.path.isdir(text_data_path):
          anw = input( 'TextData Folder already exist, may overwrite files.( Y / N)')
          if anw.lower() != 'y':
              sys.exit()
    else :
        os.makedirs(text_data_path)
    # remove the old files cuz file.write will continue from the last line.
    if os.path.isfile( text_data_path + 'trainval.txt'):
        os.remove( text_data_path + 'trainval.txt')
    if os.path.isfile( text_data_path + 'test.txt'):
        os.remove( text_data_path + 'test.txt')

    if SingleProcess: 
        print('Single Process ...')
        get_sync(SYNC)
        start = time.time()  
        '''Generate training data'''
        if Gen_train_data:
            GenData_many_targets(train_num, Initial_name_train, train_data_path, train_label_path, text_data_path)
        
        '''Generate test data'''
    
        if Gen_test_data:
            
            GenData_many_targets(test_num, Initial_name_test, test_data_path, test_label_path, text_data_path)
        end = time.time()
        print(('time : ',end - start))

    if not SingleProcess :
        print('Multiprocess...')
        
        start = time.time()
        job_queue = JoinableQueue()
        
        if Gen_train_data:
            data_path, label_path, text_path = train_data_path, train_label_path, text_data_path
            for n in range(train_num) : 
                job_queue.put( (Initial_name_train + n, data_path, label_path, text_path ))
                
        if Gen_test_data: 
            data_path, label_path, text_path = test_data_path, test_label_path, text_data_path
            for n in range(test_num) :
                job_queue.put( (Initial_name_test + n, data_path, label_path, text_path ))
              
        process_list = []

        ''' Generate data'''
            
        for p in range(2*cpu_count()-2): # PROCESS_NUM
             job_queue.put(None)
             process = Worker(job_queue)
             process_list.append(process)  
             process.start()
        
        for p in process_list : p.join()
        
        job_queue.join()
        end = time.time()   

        print('time: ', end-start)  




   
