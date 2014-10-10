# -*- encoding: utf-8 -*-
import urllib
import urllib2
import re
import os
import sys
from collections import OrderedDict

path="../100links/"
URIs=dict()
lineCount=0

##Create Graphviz.dot file
graphviz=open("graphviz.dot", "w")
graphviz.write("digraph graphviz {\n")

##Loop all Files in Path
for l in os.listdir(path):

        x=0
        output=""
        output1=""
        output2=""
        site=""
        with open(path+str(l)) as Onefile:
            for line in Onefile:
                ##Site Name
                if x == 1:
                    site=line.strip()
                    if not site in URIs:
                       URIs[site]=lineCount
                       output1=str(URIs[site])
                       lineCount=lineCount+1
               ##Grab Links
                elif x >= 3:
                    links=line.strip()
                    if not links in URIs:
                        URIs[links]=lineCount
                        output2=str(URIs[links])
                        lineCount=lineCount+1
                        
                        ##Final Output
                        if output1 and output2:
                            output=output+output1+"->"+output2+";"+"\n"
                x+=1

        ##Write to File
        graphviz.write(output)

##Create Ordered l
t=OrderedDict(sorted(URIs.items(), key=lambda t: t[1]))
for item in t.items():
    print str(item[1])+"[label="+item[0]+"]"
    graphviz.write(str(item[1])+"[label="+item[0]+"];\n")
graphviz.write("}")
del URIs

graphviz.close()
