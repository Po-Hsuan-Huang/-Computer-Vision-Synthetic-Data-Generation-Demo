#!/usr/bin/env python

# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2
from collections import defaultdict
import string
import glob

dataset = 'top_view'

perfect = []

def threshold(im, class_name, dets, thresh):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    bbxes = []

    if len(inds) == 0:
        return bbxes

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        bbxes.append((bbox[0], bbox[1], bbox[2], bbox[3], score))

    return bbxes

def draw_the_checkcode(im ,detect_checkcode):
    if detect_checkcode != None:
        height = detect_checkcode[4] - detect_checkcode[2]
        cv2.rectangle(im, (detect_checkcode[1], detect_checkcode[2]), (detect_checkcode[3], detect_checkcode[4]), (255, 255, 0))
        cv2.putText(im, detect_checkcode[0], (detect_checkcode[1], int(detect_checkcode[2]+(height/2))), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 255)

def draw_the_content(im ,bbxes, detect_checkcode):
    for bbox in bbxes:
        cv2.rectangle(im, (bbox[1], bbox[2]), (bbox[3], bbox[4]), (255, 255, 0))
        label = bbox[0]
        if label in string.lowercase:
            label = label.upper()
        height = bbox[3] - bbox[1]
        if label != '@':
            cv2.putText(im, label, (bbox[1], int(bbox[2] + (height /2))), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 255)
        else:
            cv2.putText(im, label, (bbox[1], bbox[2]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 255)




def check_code_detection(im, cls, dets, thresh):
    inds = np.where(dets[:, -1] >= thresh)[0]
    bbxes = []

    if len(inds) == 0:
        return bbxes

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        bbxes.append((bbox[0], bbox[1], bbox[2], bbox[3], score))

    return bbxes

def draw_check_code(im, cls, boxes):
    for bbox in boxes:
        cv2.rectangle(im, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 255, 0))
        cv2.putText(im, cls + ':' + str(bbox[4]), (bbox[0], int(bbox[1]+((bbox[3]-bbox[1])/2))), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 255)


def catch_check_code(net, im, image_name):
    CLASSES = map(lambda s: 'check-' + str(s) , range(10))
    CLASSES.insert(0, '__background__')
    check_code = image_name.split('_')[-1][0]
    im = im[:, :, (2, 1, 0)]
    scores, boxes = im_detect(net, im)
    # Visualize detections for each class
    CONF_THRESH = 0.5
    NMS_THRESH = 0.3
    all_bb = {}
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        bbb = check_code_detection(im, cls, dets, thresh=CONF_THRESH)
        if len(bbb) > 0:
            #  all_bb[cls] = (bbb[0:4], bbb[4])
            all_bb[cls] = bbb
    return all_bb


def find_content(net, im, image_name):
    """Detect the content inside each container number"""

    CLASSES = map(str, range(10)) + [u for u in string.lowercase]
    CLASSES.insert(0, '__background__')
    CLASSES.insert(1, 'check')

    correct_number = image_name[0:10].lower()
    print 'The correct number is %s' %(correct_number)

    correct_number = [c for c in correct_number]

    # Load the demo image
    im = im[:, :, (2, 1, 0)]

    # Detect all object classes and regress object bounds
    scores, boxes = im_detect(net, im)

    # Visualize detections for each class
    CONF_THRESH = 0.5
    NMS_THRESH = 0.3
    all_bb = {}
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        bbb = threshold(im, cls, dets, thresh=CONF_THRESH)
        if len(bbb) > 0:
            #  all_bb[cls] = (bbb[0:4], bbb[4])
            all_bb[cls] = bbb


    bbs = []
    for key, values in all_bb.iteritems():
        for value in values:
            if key == 'check':
                key = '@'
            #  bbs.append((key,) + value + (score,))
            bbs.append((key,) + value)

    yyy = sorted(bbs, key=lambda b: b[1])

    # FIXME: Faster rcnn may detect multiple class for one of the objects,
    # we can remove other classes where the boxes are overlapped

    #  remove = []
    #  while True:
        #  no_overlap = False
        #  for kk in range(0, len(yyy)):
            #  if kk + 1  >= len(yyy):
                #  no_overlap = True
                #  break
            #  rect1 = (yyy[kk][1], yyy[kk][2], yyy[kk][3], yyy[kk][4])
            #  rect2 = (yyy[kk + 1][1], yyy[kk + 1][2], yyy[kk + 1][3], yyy[kk + 1][4])
            #  overlap = almost_overlap(rect1, rect2)
            #  assert overlap == almost_overlap(rect2, rect1), 'Image %s has invalid overlapping' %(image_name)
            #  if overlap:
                #  if yyy[kk][5] > yyy[kk + 1][5]:
                    #  del yyy[kk+1]
                #  else:
                    #  del yyy[kk]
                #  break
        #  if no_overlap:
            #  break


    #  choose = ''.join([vv[0] for vv in yyy])
    choose = [vv[0] for vv in yyy]
    #  print 'check checkcode box %s' %(choose)
    idx = ''.join(choose).rfind('@')
    #  print idx
    if idx != -1:
        choose = choose[0:idx + 1]
        yyy = yyy[0:idx + 1]
        # remove other check code
        idx = ''.join(choose).rfind('@')
        idx2 = ''.join(choose).find('@')
        while idx != idx2:
            #  print idx, idx2
            del choose[idx2]
            del yyy[idx2]
            idx = ''.join(choose).rfind('@')
            #  print 'idx %d' %(idx)
            idx2 = ''.join(choose).find('@')
            #  print 'idx2 %d' %(idx2)

    choose2 = [c for c in choose]

    if len(choose2) >= 4:
        for i in range(0, 4):
            if choose2[i] == '1':
                choose2[i] = 'i'
            elif choose2[i] == '0':
                choose2[i] = 'o'
            elif choose2[i] == '8':
                choose2[i] = 'b'
            elif choose2[i] == '5':
                choose2[i] = 's'

    if len(choose2) >= 5:
        for i in range(4, len(choose2)):
            if choose2[i] == 'i':
                choose2[i] = '1'
            elif choose2[i] == 'o':
                choose2[i] = '0'
            elif choose2[i] == 'b':
                choose2[i] = '8'
            elif choose2[i] == 's':
                choose2[i] = '5'


    choose = ''.join(choose2)

    match_count = 0

    print 'what we see : %s' %(choose)
    print 'correct number : %s' %(correct_number)

    for c in choose:
        try:
            #  print 'check %s' %(c)
            index = correct_number.index(c)
            del correct_number[index]
            match_count = match_count + 1
        except ValueError:
            print 'error in check %s' %(c)
            #  continue

    print 'choose :%s' %(choose)
    print 'max_count : %d' %(match_count)

    if match_count == 10:
        perfect.append(image_name)

    return match_count, yyy


def almost_overlap(rect1, rect2):
    count = 0
    total = (rect1[2] - rect1[0]) * (rect1[3] - rect[1])
    for x in range(rect1[0], rect1[2] + 1):
        for y in range(rect1[1], rect1[3] + 1):
            if x  >= rect2[0] and x <= rect2[2] and y >= rect2[1] and y  <= rect2[3]:
                count = count + 1

    if float(count)/total  >= 0.9:
        return True
    else:
        return False



def find_container_number(net, image_name):
    """find container number."""

    CLASSES = map(str, range(10)) + sorted([u.lower() for u in ['C', 'E', 'D', 'G', 'F', 'I', 'H', 'K', 'M', 'L', 'N', 'P', 'S', 'R', 'U', 'T', 'W', 'Y']])
    CLASSES.insert(0, '__background__')
    CLASSES.insert(1, 'check')
    CLASSES.insert(2, 'number')
    CLASSES = tuple(CLASSES)
    assert len(CLASSES) == 31

    # Load the demo image
    im_file = os.path.join(cfg.DATA_DIR, dataset, image_name)
    im = cv2.imread(im_file)

    im = im[:, :, (2, 1, 0)]

    # Detect all object classes and regress object bounds
    scores, boxes = im_detect(net, im)

    CONF_THRESH = 0.5
    NMS_THRESH = 0.3
    all_bb = {}
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        all_bb[cls] = threshold(im, cls, dets, thresh=CONF_THRESH)

    numbers = all_bb['number']
    del all_bb['number']

    i = 0

    our_numbers = []
    choose = ''
    minlen = 0
    crop = None
    crops = []
    myimg = cv2.imread(im_file)
    for number in numbers:
        i = i + 1
        yyy = []
        for key, all_value in all_bb.iteritems():
            for value in all_value:
                if key != 'number':
                    if key == 'check':
                        key = '@'

                    if range_overlap(number[0], number[2], value[0], value[2]) and range_overlap(number[1], number[3], value[1], value[3]):
                        yyy.append((key,) + value )

        yyy = sorted(yyy, key=lambda b: b[1])
        names = ''.join([vv[0] for vv in yyy])
        #  if names.count('@') > 0 and names[-1] == '@':
        if True:
            nnn = image_name
            if os.path.exists('data/demo_results/' + nnn):
                nnn = nnn + str(i)

            height, width = myimg.shape[:2]

            choose = names
            minlen = len(names)
            n_width = number[2] - number[0]
            n_height = number[3] - number[1]
            extend_w = n_width * 0.3
            extend_h = n_height * 0.3
            sx = round(number[0] - extend_w)
            if sx < 0:
                sx = 0

            ex = round(number[2] + extend_w)
            if ex >= width - 1:
                ex = width - 1

            sy = round(number[1] - extend_h)

            if sy < 0:
                sy = 0
            ey = round(number[3] + extend_h)
            if ey >= height - 1:
                ey = height - 1


            #  crop = myimg[number[1]:number[3], number[0]:number[2]].copy()
            myimg = cv2.imread(im_file)
            crop = myimg[sy:ey, sx:ex].copy()
            crops.append(crop)

            #  for yy in yyy:
                #  mybbb = yy[1:]
                #  cv2.rectangle(myimg, (mybbb[0], mybbb[1]), (mybbb[2], mybbb[3]), (255,0,0), 2)

            #  cv2.rectangle(myimg, (number[0], number[1]), (number[2], number[3]), (0,0,0), 2)

    for number in numbers:
        cv2.rectangle(myimg, (number[0], number[1]), (number[2], number[3]), (0,0,0), 2)
        cv2.imwrite('data/demo_results/' + image_name + '.png', myimg)


    return crops


def range_overlap(a_min, a_max, b_min, b_max):
    '''Neither range is completely greater than the other
    '''
    overlapping = True
    if (a_min > b_max) or (a_max < b_min):
        overlapping = False
    return overlapping



def net(prototxt, model, base='ZF'):
    prototxt = os.path.join(cfg.MODELS_DIR, base, 'faster_rcnn_alt_opt', prototxt)
    caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models', model)
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    return net

def setup():
    import shutil
    if os.path.exists('data/demo_results'):
        shutil.rmtree('data/demo_results')

    if os.path.exists('data/demo_results2'):
        shutil.rmtree('data/demo_results2')

    if os.path.exists('data/demo_results3'):
        shutil.rmtree('data/demo_results3')

    if os.path.exists('data/demo_results4'):
        shutil.rmtree('data/demo_results4')

    if os.path.exists('data/demo_results2_with_checkcode'):
        shutil.rmtree('data/demo_results2_with_checkcode')


    if os.path.exists('data/miss'):
        shutil.rmtree('data/miss')

    os.mkdir('data/demo_results2_with_checkcode')
    os.mkdir('data/demo_results4')
    os.mkdir('data/demo_results3')
    os.mkdir('data/demo_results2')
    os.mkdir('data/demo_results')
    os.mkdir('data/miss')


if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    caffe.set_mode_gpu()
    caffe.set_device(0)
    cfg.GPU_ID = 0

    setup()

    # FIXME: We may not need 31 class, since 2 classes (background and container number) are sufficent enough
    # detect the container number
    number_net = net('faster_rcnn_test.pt', '31_class_no_flipped.caffemodel')
    # detect the content inside the container number
    #  content_net = net('faster_rcnn_test2.pt', '0.4M_zf_38_class.caffemodel')
    #  content_net = net('faster_rcnn_test2.pt', '0.4M_vgg16_38_class.caffemodel', base='VGG16')
    content_net = net('faster_rcnn_test2.pt', '0.5M_vgg16_38_class.caffemodel', base='VGG16')
    # detect the check code inside the container number
    check_code_net = net('faster_rcnn_test3.pt', '0.2M_with_checkcode_10_class.caffemodel')


    im_names = map(lambda b: b.split('/')[-1], glob.glob('data/%s/*' %(dataset)))

    all_count = 0

    ooo = defaultdict(list)
    ppp = defaultdict(list)

    miss = []
    check_count = 0
    correc_all_count = 0
    for im_name in im_names:
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Demo for data/demo/{}'.format(im_name)
        crops = find_container_number(number_net, im_name)
        # we may find a lot of candidate numbers
        # in order to retrive the 'only one' container number,
        # we use the content_net to detect the content inside the container number
        # and select the container number which has the most detected symbols

        if len(crops) > 0:
            count = 0
            yyy = None
            mycrop = None
            for crop in crops:
                r, yy = find_content(content_net, crop, im_name)
                if r >= count:
                    count = r
                    yyy = yy
                    mycrop = crop

            if mycrop != None:
                check_code = im_name.split('_')[-1][0]
                all_bb = catch_check_code(check_code_net, mycrop, im_name)
                all_check_code = []
                check_bbxes = []
                for key, value in all_bb.iteritems():
                    for bb in value:
                        check_bbxes.append((key.split('-')[-1],) + bb)
                detect_checkcode = None
                correct_check_code = False
                add_check = 0
                if len(check_bbxes)>0:
                    check_bbxes = sorted(check_bbxes, key=lambda b: b[1])
                    detect_checkcode = check_bbxes[-1]
                    if detect_checkcode[0] == check_code:
                        check_count = check_count + 1
                        correct_check_code = True
                        add_check = 1


                # draw each bounding box on each detected object
                draw_the_content(mycrop, yyy, detect_checkcode)
                mycrop_with_checkcode = mycrop.copy()
                draw_the_checkcode(mycrop_with_checkcode, detect_checkcode)
                cv2.imwrite('data/demo_results2/'+ im_name, mycrop)
                cv2.imwrite('data/demo_results2_with_checkcode/'+ im_name, mycrop_with_checkcode)
                ooo[count].append(im_name)
                ppp[count + add_check].append(im_name)
                correct10 = False
                if count == 10:
                    correct10 = True
                else:
                    correct10 = False

                correc_all = correct10 & correct_check_code
                if correc_all:
                    correc_all_count = correc_all_count + 1

                all_count = all_count + count
            else:
                ooo[0].append(im_name)
                ppp[0].append(im_name)
        else:
            miss.append(im_name)



    print all_count
    print float(all_count) / (len(im_names) * 10)

    print 'check code precision %f' %(float(check_count)/len(im_names))

    import shutil

    for im in miss:
        shutil.copy('data/%s/%s' %(dataset, im), 'data/miss/%s' %(im))

    for key in ooo.iterkeys():
        os.mkdir('data/demo_results3/%s' %(str(key)))

    for key in ppp.iterkeys():
        os.mkdir('data/demo_results4/%s' %(str(key)))


    all_ims = 0
    for key, value in ooo.iteritems():
        all_ims = all_ims + len(value)


    all_ims = all_ims + len(miss)

    assert all_ims == len(im_names), '%d != %d' %(all_ims, len(im_names))


    for key, value in ooo.iteritems():
        os.mkdir('data/demo_results3/%d/org' %(key))
        for v in value:
            shutil.copy('data/demo_results2/' + v, os.path.join('data', 'demo_results3', str(key), v))
            shutil.copy('data/%s/' %(dataset) + v, os.path.join('data', 'demo_results3', str(key), 'org', v))
        print key, len(value)
        ratio = float(len(value))/len(im_names) * 100
        print '%s:%s%%' %(key, str(ratio))

    print '--------------------Add check code-----------------------------------------'

    for key, value in ppp.iteritems():
        os.mkdir('data/demo_results4/%d/org' %(key))
        for v in value:
            shutil.copy('data/demo_results2_with_checkcode/' + v, os.path.join('data', 'demo_results4', str(key), v))
            shutil.copy('data/%s/' %(dataset) + v, os.path.join('data', 'demo_results4', str(key), 'org', v))
        print key, len(value)
        ratio = float(len(value))/len(im_names) * 100
        print '%s:%s%%' %(key, str(ratio))
