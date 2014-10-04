# -*- encoding: utf-8 -*-

import urllib2
import re
import subprocess
from subprocess import call
import md5
import os

##New Dir for Output
dir1_name='../Pages'
try:
    os.makedirs(dir1_name)
		
##Grab Final List- 1000 Links
file1=open("FinalList.txt","r")

lineCount=0
for line in file1:
    lineCount=lineCount+1

    ##Remove \n
    Oneline=line.rstrip("\n")

    ##Curl
    try:
      r = urllib2.Request(Oneline)
      l = urllib2.urlopen(r)

      ##Check for 200 Response
      if l.code==200:
       allData=l.read()

       ##Create Hash, md5
       test=md5.new(Oneline)
       filename=test.hexdigest()
       
       with open(os.path.join(dir1_name,filename+'.txt'), 'w') as file3:
          file3.write(allData)
       
       ##Lynx
       cmd = os.popen("lynx -dump -force_html %s %s" %(line,filename))
       output_no_tags = cmd.read()
       cmd.close()
       with open(os.path.join(dir1_name,filename+'.processed.txt'), 'w') as file4:
          file4.write(output_no_tags)
            
file1.close()
