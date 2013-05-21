# -*- coding: utf-8 -*-
"""
Created on Mon May 06 15:06:36 2013

@author: lyako297
"""
# gives the current folder to python
from __future__ import division
from bs4 import BeautifulSoup
#import nltk, re#, pprint
import urllib2
import pickle
import os# ,sys
## wd for script running : 
#basedir, filename = os.path.split(os.path.abspath(__file__))
#print "running from", basedir
#print "file is", filename

# wd for coding
# os.chdir("\\\\neptunus.helix.ida.liu.se\\lyako297\\Documents\\atlas_sync\\732A47 Textmining\\lab\\lab 1 information retrival")
os.chdir("D:\\Dropbox\\IDA_LIU\\732A47 Textmining\\lab\\lab 1 information retrival")
basedir = os.getcwd()

base_url = "http://www.appbrain.com"

#imitate a mozilla 5.0 web-browser
headers = { 'User-Agent' : 'Mozilla/5.0' }


def read_from_file(filename,wd=""):
    infile = open(filename,'rb')
    lista = pickle.load(infile)
    infile.close()
    return(lista)

# full_dir = os.listdir(dirname)
# del full_dir


def downloadthread(fil):
    apps_links = read_from_file(fil)
    for link in apps_links[1:3]:
    #    link = apps_links[1] # dev version of for loop
        req = urllib2.Request("%s%s" % (base_url,link), None, headers)
        html_doc = urllib2.urlopen(req).read()
        ################        Title extract
        startstring = '<title>'
        start = html_doc.find(startstring)+len(startstring)
        endstring='| AppBrain Android Market</title>'
        end = html_doc.find(endstring)
        Title = html_doc[start:end]        
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
        subdir = "\\fulldescriptions\\" + fil[1:fil.find(".")]+"\\"
        path = basedir+subdir
        filename = path+Title+".txt"
        if not os.path.exists(path): # if folder does not exist create it.
            os.makedirs(path)
        with open(filename, "w") as txtfile:
            txtfile.write(description.encode('utf8'))
        print("link:%s done" % link)

pklfiles = [file for file in os.listdir(basedir) if file.endswith("pkl")]
for fil in pklfiles:
    downloadthread(fil)


raw_input("Script Done !! \nPress Enter key to exit")
# this is for a console "Run"
