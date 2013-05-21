# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 14:36:41 2013

@author: lyako297
"""

import thread
import time


que = ["Lyam","Dolk"]

# Define a function for the thread
def crawler_thread(threadName):
   print "%s: %s" % ( threadName, "hi\n" ) 

# Create two threads as follows
try:
   thread.start_new_thread(crawler_thread, ("Thread-1", ) )
   thread.start_new_thread(crawler_thread, ("Thread-2", ) )
except:
   print "Error: unable to start thread"

while 1:
   pass