# -*- encoding: utf-8 -*-

import urllib
import urllib2
import re
import os
import sys
import md5
import BeautifulSoup
import subprocess
from subprocess import call

path="../100Links"

##New Dir for Links
try:
    os.makedirs(path)
except OSError:
    if os.path.exists(path):
        pass

file1=open("FinalList.txt","r")
lineCount=0

for line in file1:
    lineCount=lineCount+1
    
    if lineCount<=100:
        Oneline=line.rstrip("\n")
        
        ##Beautiful Soup
        try:
            request = urllib2.Request(Oneline)
            response = urllib2.urlopen(request)
            soup = BeautifulSoup.BeautifulSoup(response)
        
        ##Hash 
        test=md5.new(Oneline)
        hashfilename=test.hexdigest()
        
        internallinklist=[]
        del internallinklist[:]
        
        ##Inner Links
        for a in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            link2=a['href']
            
            #No Duplicate Links
            if "png" not in link2 and "jpg" not in link2 and "#" not in link2 and "javascript" not in link2 and link2 not in internallinklist:
                internallinklist.append(link2)

        if not internallinklist:
            lineCount=lineCount-1
        
        else:
            with open(os.path.join(path,hashfilename), 'w') as file4:
				file4.write("site:")
                file4.write("\n")
                file4.write(Oneline)
                file4.write("\n")
                file4.write("links:")
                file4.write("\n")
                
                for item in internallinklist:
                    file4.write(item)
                    file4.write("\n")
        sys.exit()

file1.close()
file4.close()