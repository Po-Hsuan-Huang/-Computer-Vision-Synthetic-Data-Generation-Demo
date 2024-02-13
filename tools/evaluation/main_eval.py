# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pickle, os
from voc_eval import voc_eval, parse_rec
import numpy as np
import matplotlib.pyplot as plt



def write_voc_results_file( all_boxes, classes, image_index):
    for cls_ind, cls in enumerate(classes):
        if cls == '__background__':
            continue
        print(('Writing {} VOC results file'.format(cls)))
        filename = '{:s}.txt'
        det_path = os.path.join(
            'detections',
            filename).format(cls)
        
        with open(det_path, 'wt') as f:
            for im_ind, index in enumerate( image_index):
                dets = all_boxes[cls_ind][im_ind]
                if dets == []:
                    continue
                # the VOCdevkit expects 1-based indices
                for k in range(dets.shape[0]):
                    f.write('{:s} {:.3f} {:.1f} {:.1f} {:.1f} {:.1f}\n'.
                            format(index, dets[k, -1],
                                   dets[k, 0] + 1, dets[k, 1] + 1,
                                   dets[k, 2] + 1, dets[k, 3] + 1))

def do_python_eval( ovthresh=0.5, output_dir = 'output'):
    classes = ('__background__', # always index 0
                        'tag',)+ tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')    

    annopath = os.path.join(
        'annotations',
        '{:s}.xml')
    imagesetfile = os.path.join(
        'ImageSets',
        'Main',
        'test.txt')   
    
    cachedir = os.path.join('./annotations_cache')
    aps = []
    dic_pred = [0]
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    for k, cls in enumerate(classes):
        if cls == '__background__':
            continue
        
        filename = './detections/' + str(cls)+'.txt'


        rec, prec, ap, count = voc_eval(
            filename, annopath, imagesetfile, cls, cachedir, ovthresh=0.5)
        aps += [ap]
        print(('detectoin count for {} = {:.4f}'.format(cls, int(count))))
        dic_pred.append(int(count))
#        with open(os.path.join(output_dir, cls + '_pr.pkl'), 'w') as f:
#            cPickle.dump({'rec': rec, 'prec': prec, 'ap': ap}, f)
    return dic_pred 

def gt_count():

    annopath = os.path.join(
        'annotations',
        '{:s}.xml')
    imagesetfile = os.path.join(
        'ImageSets',
        'Main',
        'test.txt')    
    
    classes = ('__background__', # always index 0
                        'tag',)+ tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    
    dic_gt =np.zeros(len(classes))
    with open(imagesetfile) as f:
        filenames = [x.strip() for x in f.readlines()]
        
    objects_set = [parse_rec(annopath.format(s)) for s in filenames]
        
    for p, j in enumerate(classes):
        for objects in objects_set:
            for object_struct in objects:
                if object_struct['name'] == j:
                   dic_gt[p] +=1    
    
    return dic_gt
#%%
if __name__=='__main__':
    image_index = []
    with open('ImageSets/Main/test.txt','r') as f:
        for line in f:
            line = line.strip('\n')
            image_index.append(line)
        
    
    classes = ('__background__', # always index 0
                        'tag',)+ tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                
    with open('detections/detections.pkl', 'rb') as f1:
        imgbox = pickle.load(f1)
    
    write_voc_results_file(imgbox, classes, image_index)

    dic = do_python_eval()
    dic_gt =gt_count()
    
    plt.figure()
    bins = np.linspace(0, 39, 38)
    plt.bar(bins, dic, alpha=0.5, color ='red')
    plt.bar(bins, dic_gt, alpha=0.5, color = 'green')
    plt.legend('detect','gt')
    plt.show()

    plt.figure()
    bins = np.linspace(0, 39, 38)
    plt.bar(bins, dic/dic_gt, alpha=0.5, color = 'green')
    plt.legend('detect','gt')
    plt.show()            
    
        
    
        
