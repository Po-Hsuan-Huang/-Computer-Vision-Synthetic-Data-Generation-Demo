#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:34:42 2017

@author: pohsuanh
"""
#%%

from multiprocessing import JoinableQueue as MJ
import time
from multiprocessing import Process as MP
import numpy as np


class Worker(MP):          
    
      def __init__(self, queue):
          MP.__init__(self)
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
                  print(('working... ',self.name, job))
                  time.sleep(0.08)
                  self.queue.task_done()              
          

if __name__ == '__main__':
    
    q = MJ()
    
    for i in range(1,100): q.put(i)

    plist = []
    
    for i in range(15):
        p = Worker(q)
        plist.append(p)
        q.put(None)
        
    for i in plist: i.start()
            
    for i in plist: i.join()

    q.join()
    
    
    print('finished.')
        
