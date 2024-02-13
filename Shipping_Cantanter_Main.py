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
If not exist yet, the program create a new folder for you.c

Specify the size of training set and test set, and the naming follows the 
order that can be used by pva-fast-rcnn.

https://github.com/sanghoon/pva-faster-rcnn

training set : 1 ~ trainset_size

test set : trainset_size + 1 ~ trainset_size + testset_size 


'''
import time
from multiprocessing import Process, cpu_count, Manager, JoinableQueue
from gen_images_many_targets import GenData_many_targets, get_gen_type, get_sync_batch, get_overwrite, get_sync
import os, glob, sys
import numpy as np

def work(n, n0,  data_path, label_path, text_path): 
            global start
            print('gen-data...', n, n0)        
            GenData_many_targets(n, n0, data_path, label_path, text_path)
            print('gen-data2...')        

            end = time.time()   

            print('time: ', end-start)          

if __name__ == '__main__':
    global start
    
    Gen_train_data = True
    Gen_test_data = False
    SingleProcess = False
    Overwrite = False
    SYNC = False
    # number of training data 
    
    train_num = 400000
    
    # number of testing data
    
    test_num = 1
    
    # batchsize sync to remote
    
    SycBatchSize = 200
    
    # initial name for training
    Initial_name_train = 10
    
    # initial name for testing
    Initial_name_test = train_num
        
    get_overwrite(Overwrite)
        
    get_gen_type(Gen_train_data, Gen_test_data)
    
    get_sync_batch(SycBatchSize)
    


   
    ''' The folders must be created beforehand, remember not to overwrite'''
    
    # trian annotation data path
    train_label_path = '/home/acer/Documents/Marathon/data/Annotations/TrainSet8/' 
    # test annotation data path
    test_label_path = '/home/acer/Documents/Marathon/data/Annotations/TestSet8/' 
    # train_data_output_path
    train_data_path = '/home/acer/Documents/Marathon/data/JPEGImages/TrainSet8/'
    # test_data_output_path
    test_data_path =  '/home/acer/Documents/Marathon/data/JPEGImages/TestSet8/'
    # index file tracking whom should be trained and whom should be tested
    text_data_path = '/home/acer/Documents/Marathon/data/ImageSets/Main/8/' 

    
    ''' Check if the folders exist && empty. If not, create a new folder.'''
    if Gen_train_data :
        print('Gen_train_data')
    
        if os.path.isdir(train_data_path):
            if len(glob.glob(train_data_path +"*.jpg")) != 0 :
                 anw = raw_input( ' Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
                 if anw.lower() != "y":
                     sys.exit()
        else:
            os.makedirs(train_data_path)
            
        if os.path.isdir(train_label_path):
            if len(glob.glob(train_label_path +"*.xml")) != 0 :
                 anw = raw_input( ' Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
                 if anw.lower() != "y":
                     sys.exit()
        else:
            os.makedirs(train_label_path)
    
    if Gen_test_data:
        print('Gen_test_data')
        
        if os.path.isdir(test_data_path):
            if len(glob.glob(test_data_path +"*.jpg")) != 0 :
                 anw = raw_input( ' Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
                 if anw.lower() != "y":
                     sys.exit()
        else:
            os.makedirs(test_data_path)
        
        
        
        if os.path.isdir(test_label_path):
            if len(glob.glob(test_label_path +"*.xml")) != 0 :
                 anw = raw_input( ' Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
                 if anw.lower() != "y":
                     sys.exit()
        else:
            os.makedirs(test_label_path)
    
    '''Check text_path''' 
    if os.path.isdir(text_data_path):
          anw = raw_input( 'Folder already exist, may overwrite files.[y/n]')
          if anw.lower() != 'y':
              sys.exit()
    else :
        os.makedirs(text_data_path)
    # remove the old files cuz file.write will continue from the last line.
    if os.path.isfile( text_data_path + 'trainval.txt'):
        os.remove( text_data_path + 'trainval.txt')
    if os.path.isfile( text_data_path + 'test.txt'):
        os.remove( text_data_path + 'test.txt')

#%%
    if SingleProcess: 
        get_sync(SYNC)

        '''Generate training data'''
        if Gen_train_data:
            GenData_many_targets(train_num, Initial_name_train, train_data_path, train_label_path, text_data_path)
        
        '''Generate test data'''
    
        if Gen_test_data:
            
            GenData_many_targets(test_num, Initial_name_test, test_data_path, test_label_path, text_data_path)
            
     
    if not SingleProcess:
        start = time.time()
        jobs =[]
        '''Generate data'''
        if Gen_train_data:

            Max_core = cpu_count()-1
#            Max_core = 1
            assert train_num >= Max_core, "test_num must be larger than core numbers"  
            n = train_num/Max_core
            
            for k in range( Max_core):
                
                n = train_num/Max_core
                n0 = Initial_name_train + k*n
                 
                if k == Max_core-1 : 
                    get_sync(SYNC) # synching is executed in the parent process 
                    print('ParentProcess...')
                    GenData_many_targets(train_num, Initial_name_train, train_data_path, train_label_path, text_data_path)
                elif k == 0 :
                    n = train_num/Max_core + train_num % Max_core
                    get_sync(False)
                    p = Process(target=work, args = (n, n0, train_data_path, train_label_path, text_data_path))
                    jobs.append(p)
                    p.start()
                    print('ChildProcess...',k)
                else:
                    get_sync(False)
                    p = Process(target=work, args = (n, n0, train_data_path, train_label_path, text_data_path))
                    jobs.append(p)
                    p.start()
                    print('ChildProcess...',k)

                print('core:',k)
            
            
            for p in jobs:
                p.join()

        if Gen_test_data:
 
            Max_core = cpu_count() -1
            
            assert test_num >= Max_core, "test_num must be larger than core numbers"  
            n = test_num/Max_core
    
            for k in range( Max_core ):
            
                n = test_num/Max_core
                n0 = Initial_name_test + k*n

                np.random.seed()

                if k == Max_core-1 : 
                    get_sync(SYNC)
                    print('ParentProcess...')
                    GenData_many_targets(n, Initial_name_test, test_data_path, test_label_path, text_data_path)

                elif k == 0 :
                    n = train_num/Max_core + train_num % Max_core
                    get_sync(False)
                    p = Process(target=work, args = (n, n0, train_data_path, train_label_path, text_data_path))
                    jobs.append(p)
                    p.start()
                    print('ChildProcess...',k)
                else:
                    get_sync(False)
                    p = Process(target = work , args = (n, n0, test_data_path, test_label_path, text_data_path))
                    jobs.append(p)
                    p.start()
                    print('ChildProcess...', k)

                print('core:',k)

            
            for p in jobs:
                p.join()




