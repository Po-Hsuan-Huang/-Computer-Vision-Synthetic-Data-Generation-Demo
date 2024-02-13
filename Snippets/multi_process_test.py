#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:25:09 2017

@author: pohsuan
Multiprocess JoinableQueue Practice

"""
from multiprocessing import Process, cpu_count, JoinableQueue



def worker(queue):
      job = queue.get()
      print job
      queue.task_done()

if __name__ == '__main__':

     job_queue = JoinableQueue()
     # mock to put ads inside
     jobs = range(100)         

     for job in jobs : job_queue.put(job)
      
     process_list = []

     for p in range(cpu_count()-1): # PROCESS_NUM
         
         process = Process(target=worker, args = (job_queue,))
         process_list.append(process)     
         process.start()
         
     while not job_queue.empty():
         for i, p in enumerate(process_list):
             if not job_queue.empty():
                 p.run()
                 print p.name
             else:
                 print 'empty'
                 break
                     
     for p in process_list: p.join()            


