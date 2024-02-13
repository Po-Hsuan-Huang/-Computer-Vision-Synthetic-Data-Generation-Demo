#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:04:35 2017

@author: pohsuanh
"""

from give_me_the_code import *
import time
from multiprocessing import Process, Queue, Pool, JoinableQueue
import multiprocessing
import lmdb
import numpy as np
import argparse

start_time = time.time()
parser = argparse.ArgumentParser(description='Generate container number')
parser.add_argument('--num', type=int, dest='num_images', help='number of images', required=True)
parser.add_argument('--noise', dest='with_noise', action='store_true', help='add perlin noise')
parser.add_argument('--column', dest='column_side', action='store_true', help='gen column number')
parser.add_argument('--noise_max', type=int, dest='noise_max', default=30 , help='the large value will produce very damaged image')
parser.add_argument('--noise_map', type=int, dest='num_noise_map', default=300 , help='the number of noise maps for each process')
parser.add_argument('--db_name', dest='db_name', help='database name', required=True)
parser.set_defaults(with_noise=False)
args = parser.parse_args()

image_set = 'train'
db_name = str(int(round(time.time()) * 1000)) + '-%s' %(args.db_name)
#  db_name = 'mydb'

image_db = os.path.join(image_set, 'Image')
index_set = os.path.join(image_set, 'Index')
annotation_db = os.path.join(image_set, 'Annotation')

assert not os.path.exists(image_set), 'Path {} exist'.format(image_set)

os.makedirs(image_db)
os.makedirs(index_set)
os.makedirs(annotation_db)


# get all background
bg_list = glob.glob('./background/**/out/*')
assert len(bg_list)  >= 8000

# set number of images
num_images = args.num_images
side = 0
if args.column_side:
    side = 1

# this shold always be 1
filenames = [('{:08d}'.format(num), side) for num in range(1, num_images + 1)]
bgs = np.random.randint(0, len(bg_list), num_images)

WITH_NOISE = args.with_noise


class Writer(multiprocessing.Process):
    def __init__(self, result_queue, num):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue
        self._num = num
    def run(self):
        proc_name = self.name

        image_env = lmdb.open(os.path.join(image_db , db_name), map_size=1000*1000*1000*100)
        image_txn = image_env.begin(write=True)

        annotation_env = lmdb.open(os.path.join(annotation_db , db_name), map_size=1000*1000*1000*100)
        annotation_txn = annotation_env.begin(write=True)

        count = 0

        while count < num:
            filename, image, annotation = self.result_queue.get()
            print(('%s receive %s' % (proc_name, filename)))
            image_txn.put(filename, image)
            annotation_txn.put(filename, annotation)
            count = count + 1
            print(count)

            if count % 1000 == 0:
                image_txn.commit()
                annotation_txn.commit()
                image_txn = image_env.begin(write=True)
                annotation_txn = annotation_env.begin(write=True)


        print(('writer %s: commit last' % proc_name))
        if count % 1000 != 0:
            image_txn.commit()
            annotation_txn.commit()

        image_env.close()
        annotation_env.close()
        print(('writer %s: Exiting' % proc_name))


class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        np.random.seed()
        im_noises = None
        if WITH_NOISE:
            im_noises = []
            # set the number of noise maps here
            for i in range(args.num_noise_map):
                im_noises.append(give_me_noise(args.noise_max))
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print(('%s: Exiting' % proc_name))
                self.task_queue.task_done()
                break
            print(('%s: %s' % (proc_name, next_task)))
            answer = next_task(im_noises, bg_list)
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task():
    def __init__(self, handler, filename, bg_no):
        self.handler = handler
        self.filename = filename
        self.bg_no = bg_no
    def __call__(self, im_noises, bg_list):
        return self.handler(self.filename, im_noises, bg_list, self.bg_no)




# for debug use
#  b = open('background.txt', 'w')
#  for bg_no in bgs:
    #  b.write(bg_list[bg_no])
    #  b.write('\n')

assert len(filenames) == num_images

index_file = open(os.path.join(index_set, db_name) + '.txt', 'w')
for filename in filenames:
    index_file.write("{}\n".format(filename[0]))


tasks = JoinableQueue()
results = Queue()
num_consumers = multiprocessing.cpu_count() * 2
print(('Creating %d consumers' % num_consumers))
consumers = [ Consumer(tasks, results) for i in range(num_consumers) ]
for w in consumers:
    w.start()

writer = Writer(results, len(filenames))
writer.start()

for i in range(0, len(filenames)):
    tasks.put(Task(give_me_SCC_images, filenames[i], bgs[i]))
tasks.join()


for i in range(num_consumers):
    tasks.put(None)

writer.join()
print(("--- %s seconds ---" % (time.time() - start_time)))