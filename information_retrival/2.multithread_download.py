# -*- coding: utf-8 -*-
"""
Created on Tue May 07 20:23:17 2013

@author: Lyam Dolk
lyamdolk@gmail.com
"""
from __future__ import division
from bs4 import BeautifulSoup
import urllib2
import pickle
import Queue
import threading
import time #relic from example probably not needed in current code
import os, sys
import re
#basedir, filename = os.path.split(os.path.abspath(__file__))
#os.chdir("D:\\Dropbox\\IDA_LIU\\732A47 Textmining\\lab\\lab 1 information retrival")
os.chdir("\\\\neptunus.helix.ida.liu.se\\lyako297\\Documents\\atlas_sync\\732A47 Textmining\\lab\\lab 1 information retrival")
basedir = os.getcwd()

base_url = "http://www.appbrain.com"
headers = { 'User-Agent' : 'Mozilla/5.0' }
exitFlag = 0

def read_from_file(filename,wd=""):
    infile = open(filename,'rb')
    lista = pickle.load(infile)
    infile.close()
    return(lista)

def write_to_file(filename,path,obj):
    fullpath= path+filename+'.pkl'
    outfile = open(fullpath, 'wb') # filename
    pickle.dump(obj, outfile) #dump to file
    outfile.close()
    print "variable written to:"
    print fullpath # verification

def download_link(link):
    req = urllib2.Request("%s%s" % (base_url,link), None, headers)
    try:
        html_doc = urllib2.urlopen(req).read()
    except:
        print "Downdload failed"   
        return()
    ################     item   Title extract
    startstring = '<title>'
    start = html_doc.find(startstring)+len(startstring)
    endstring='| AppBrain Android Market</title>'
    end = html_doc.find(endstring)
    title = html_doc[start:end]        
    ################        Description extract
    startstring = '<div class="app_descriptiontab">'
    start = html_doc.find(startstring)+len(startstring)
    endstring='<div style="position: absolute; right: 0px; bottom: 0px">'
    end = html_doc.find(endstring)
    description = html_doc[start:end]
    ################ 
    description = description.strip() # get rid of whitespace
    description = BeautifulSoup(description)
    description = description.get_text() # get rid of html
    path = basedir+"\\fulldescriptions\\"
    filename= re.sub(r'\W+', '', title)# clean filename
    if not os.path.exists(path): # if folder does not exist create it.
        os.makedirs(path)
    try:
        info = (("Title",title.encode('utf8')),("Description:",description.encode('utf8')))
        write_to_file(filename,path,info)
    except Exception as ex:
        queueLock.acquire()
        print "Write failed"
        failQueue.put((link,sys.exc_info()[0],ex))
        queueLock.release()
#        global exitFlag
#        exitFlag = 1

print "80"
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.q)
        print "Exiting " + self.name
print "91"
def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            link = q.get()
            print workQueue.qsize()
            queueLock.release()
            #print "%s processing %s " % (threadName, item[0])
            download_link(link)
        else:
            queueLock.release()
        time.sleep(1)
print "104"

# number of threads to initiate
n = 100
threadList=[]
for i in range(1,n+1):
    threadList.append("Thread-%s"%i)

#threadList = ["Thread-1", "Thread-2", "Thread-3"]
linkList=[]
pklfiles = [file for file in os.listdir(basedir) if file.endswith("pkl")]
#fil = pklfiles[1]
for fil in pklfiles:
    apps_links = read_from_file(fil)
    #link = apps_links[1]
    for link in apps_links:
        linkList.append(link)

#linkList = list(set(linkList)) # remove duplicates

#nameList = ["One", "Two", "Three", "Four", "Five"]
print "Que creation starting"
queueLock = threading.Lock()
workQueue = Queue.Queue(len(linkList))
failQueue = Queue.Queue(len(linkList)) # save items that fail
threads = []
threadID = 1
print "Setup done"
# Fill the queue
queueLock.acquire()
print "Queuelock, acquired"
for link in linkList:
    workQueue.put(link)
#    print item[0] + " added to Queue"
queueLock.release()
print "Queuelock, Relseased, que filled."
# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

print "Main is waiting for que to empty"
# Wait for queue to empty
while not workQueue.empty() and exitFlag == 0:
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()

fails =[(1,2,3)]
while not failQueue.empty():
    fails.append(failQueue.get())

write_to_file("failed items",basedir+"\\",fails)
#len(fails) # 141 fails on my runs

print "Exiting Main Thread"