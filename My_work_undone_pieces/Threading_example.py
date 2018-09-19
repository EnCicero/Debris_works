# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 15:39:08 2018

@author: EP
"""

import threading
import time
import random
import numpy as np
import h5py

f=h5py.File('threading_demo.hdf5','w')
dset=f.create_dataset('data',(3,1024),dtype='f')
lock=threading.RLock()

class ComputeThread(threading.Thread):
    def __init__(self,axis):
        self.axis=axis
        threading.Thread.__init__(self)
    def run(self):
        for idx in range(1024):
            random_number=random.random()*0.01
            time.sleep(random_number)
            print(self.axis)                     
            with lock:
                dset[self.axis,idx]=random_number
thread1=ComputeThread(0)
thread2=ComputeThread(1)
thread3=ComputeThread(2)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()

f.close()
