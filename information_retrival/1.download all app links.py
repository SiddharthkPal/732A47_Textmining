# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:25:12 2013
@author: Lyam Dolk
"""

from __future__ import division
from bs4 import BeautifulSoup
import urllib2

#save to file
import pickle
import os
# where to save file.
 
os.chdir(sys.argv[0])
#os.chdir("\\\\neptunus.helix.ida.liu.se\\lyako297\\Documents\\atlas_sync\\732A47 Textmining\\lab\\lab 1 information retrival")
os.getcwd()

def write_to_file(filename,obj):
    outfile = open(filename+'.pkl', 'wb') # filename
    bitstream = pickle.dump(obj, outfile)
    outfile.close()
    print "variable written to:"
    print os.getcwd()+"\\"+filename+'.pkl' # verification

# write_to_file("app_links",app_links)


#del app_links

#To read it back:
# debug 
# filename = "app_links"
def read_from_file(filename,wd=""):
    infile = open(filename+".pkl",'rb')
    lista = pickle.load(infile)
    infile.close()
    return(lista)

#Now the web-page is saved in html-format in the variable html
#Top apps gives 200 apps
base_url = "http://www.appbrain.com/"

#imitate a mozilla 5.0 web-browser
headers = { 'User-Agent' : 'Mozilla/5.0' }

#live list "real list"
category_list = ["/apps/hot-week/","/apps/hot-week/books-and-reference/","/apps/hot-week/business/","/apps/hot-week/comics/","/apps/hot-week/communication/","/apps/hot-week/education/","/apps/hot-week/entertainment/","/apps/hot-week/finance/","/apps/hot-week/health-and-fitness/","/apps/hot-week/lifestyle/","/apps/hot-week/media-and-video/","/apps/hot-week/medical/","/apps/hot-week/music-and-audio/","/apps/hot-week/news-and-magazines/","/apps/hot-week/personalization/","/apps/hot-week/photography/","/apps/hot-week/productivity/","/apps/hot-week/shopping/","/apps/hot-week/social/","/apps/hot-week/sports/","/apps/hot-week/tools/","/apps/hot-week/transportation/","/apps/hot-week/travel-and-local/","/apps/hot-week/weather/","/apps/hot-week/libraries-and-demo/"]

#if debug == True:
#    category_list = category_list[0:1]   # reduces list to a single category for testin purpuses
#    i = 0

# get all the app links
for category in category_list:
    app_links=[]    
    print(category)
    for i in range(0,200,10): # range(0,200,10) is full range
        print(i)
        #create the request (the url+data (which is empty)+header
        req = urllib2.Request("%s%s?o=%i" % (base_url,category,i), None, headers)
        html_doc = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html_doc)
        print("html downloaded")
        for tag in soup.find_all('a',href=True):
            tag = str(tag)
            start = tag.find('href="')+6
            end = tag[start:len(tag)].find('"')+start
            tag = tag[start:end]
            if tag.startswith("/app/"):
#                print ("app found: %s  in cat: %s "% (tag,category))
#                app_links.append((tag,category))
                app_links.append(tag)
    filename = category.replace("/","_")
    filename= filename[:-1] # remove the last underscore _
    write_to_file(filename,app_links)