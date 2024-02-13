'''

This file shall only be run after running filter.py

generate .txt files needed for fastrcnn training.

ImageSetss/Main/trainval.txt
ImageSet/Main/test.txt 

are two index files tracking which image to be used during training and testing.
This help weed out faulty data points.  

The broken data's indicies are stored in broken.txt 



parameters :
    isTrain : Boolean
        if the broken files are in train data
    isTest : Boolean
        if the broken files are in test data
    folder : string
        name of the destination folder containing the .txt file

-----------------------------------------------------------------
Note : 
    start, stop might need to change according to the amount of
    samples you generated.
    
    the default is 10000 trainig data, 1000 testing data.
    
'''
import glob, sys, os
import numpy as np
    
''' Parameters'''
# range of index numbers  
isTrain = False 
isTest = True 
#folder 
folder = 0

SINGLE_GEN = True

#%%    
# destination 
'''SINGLE GEN'''
if isTrain:
    start = 10110
    stop  = 10130
    dest = 'trainval.txt'
if isTest:
    start = 10001
    stop  = 10110
    dest = 'test.txt'
    
'''MULTI_GEN'''    
files = sorted(glob.glob('/home/pohsuan/Documents/Marathon2017/data/Annotations/TrainSet'+str(folder)+'/*.xml' ))

print 'file not empty ', len(files)

#%%
list_ecpt = []
list_valid = []

with open('/home/acer/Documents/Marathon/data/ImageSets/broken.txt', 'r') as f :
    exceptions = list(f)
#%%   
data_path = '/home/acer/Documents/Marathon/data/ImageSets/Main/'+ str(folder) + '/'
if os.path.isdir(data_path):
    if len(glob.glob(data_path +"*.txt")) != 0 :
         anw = raw_input( ' Folder not empty ! Want to overwrite ? (Y / N)')  # not empty list considered true
         if anw.lower() != "y":
             sys.exit()
else:
    os.makedirs(data_path)


with open(data_path + dest, 'w') as g:
#%% 
    exceptions = np.sort(exceptions)
    print 'size of broken files ', len(exceptions)
    for x in exceptions:
        x = int(x)
        list_ecpt.append(x) 
        
    if SINGLE_GEN:
        for x in range(start, stop + 1 ):
            if list_ecpt:
                if (x != list_ecpt[0]) :
                    list_valid.append(x)
                    filename = '{:07d}'.format(x)
                    g.write(filename + '\n')
                else:
                    list_ecpt.pop(0)
            else:
                 list_valid.append(x)
                 filename = '{:07d}'.format(x)
                 g.write(filename + '\n')
    else:
        for x in files:
            x = x.split('.jpg')[0]
            x = x.split('/home/acer/Documents/Marathon/data/JPEGImages/TrainSet'+str(folder))[1]

            x = int(x)
            if list_ecpt:
                if (x != list_ecpt[0]) :
                    list_valid.append(x)
                    filename = '{:07d}'.format(x)
                    g.write(filename + '\n')
                else:
                    list_ecpt.pop(0)
            else:
                 list_valid.append(x)
                 filename = '{:07d}'.format(x)
                 g.write(filename + '\n')


##%%    
## destination 
#if isTrain:
#    start = 1
#    stop  = 10000
#    dest = 'trainval.txt'
#    generate(start, stop, dest, folder)
#
#if isTest:
#    start = 10001
#    stop  = 10045
#    dest = 'test.txt'
#    generate(start, stop, dest, folder)
