# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:13:08 2013

@author: lyako297
"""
from __future__ import division
import pickle
import os, sys
import nltk
from nltk.book import FreqDist
#import re

def read_from_file(filename):
    infile = open(filename,'rb')
    obj = pickle.load(infile)
    infile.close()
    return(obj)

def write_to_file(filename,path,obj):
    fullpath= path+filename+'.pkl'
    outfile = open(fullpath, 'wb') # filename
    pickle.dump(obj, outfile) #dump to file
    outfile.close()
    print "variable written to:"
    print fullpath # verification

os.chdir("\\\\neptunus.helix.ida.liu.se\\lyako297\\Documents\\atlas_sync\\732A47 Textmining\\lab\\lab 1 information retrival")
basedir = os.getcwd()

def preprocess(text):
#    text="\fd"
#    cleantext = text.replace("\\"," \\")
    cleantext=text
    return(cleantext)

def normalize(tokens):
    tokens = [token.lower() for token in tokens] # removes upper cases
    return(tokens)

#files to process
path = basedir+"\\fulldescriptions\\"
appfiles = [file for file in os.listdir(path) if file.endswith("pkl")]
raw_tf_index = nltk.defaultdict(dict)
for fil in appfiles[0:100]:
    print fil
    file_content=read_from_file(path+fil)
    app_title = file_content[0][1]
    description = file_content[1][1]
    # normalazation
    tokens = nltk.word_tokenize(description)
    description = normalize(tokens)
    #create Term freq structure
    tf= FreqDist(tokens)
    for token in set(tokens):
        raw_tf_index[token][app_title]=tf[token]

