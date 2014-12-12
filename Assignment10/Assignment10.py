# -*- coding: utf-8 -*-
import feedparser
import re
import sys
import math
from operator import itemgetter

def getwords(doc):
  splitter=re.compile('\\W*')
  doc=re.compile(r'<[^>]+>').sub('',doc)  
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  word=[]
  for W in dict([(w,1) for w in words]):
	word.append(W)
  return word
  
class classifier:
  def __init__(self,getfeatures,filename=None):
    self.fc={}
    self.cc={}
    self.getfeatures=getfeatures

  def incf(self,f,cat):
    self.fc.setdefault(f,{})
    self.fc[f].setdefault(cat,0)
    self.fc[f][cat]+=1

  def incc(self,cat):
    self.cc.setdefault(cat,0)
    self.cc[cat]+=1

  def fcount(self,f,cat):
    if f in self.fc and cat in self.fc[f]:
     return float(self.fc[f][cat])
    return 0.0

  def catcount(self,cat):
    if cat in self.cc:
     return float(self.cc[cat])
    return 0

  def categories(self):
    return self.cc.keys( )

  def train(self,item,cat):
    features=self.getfeatures(item)
    for f in features:
      self.incf(f,cat)
    self.incc(cat)
  	
  def fprob(self,f,cat):
    if self.catcount(cat)==0: return 0
    return self.fcount(f,cat)/self.catcount(cat)

  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    basicprob=prf(f,cat)
    totals=sum([self.fcount(f,c) for c in self.categories()])
    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp

class fisherclassifier(classifier):
  def cprob(self,f,cat):
    clf=self.fprob(f,cat)
    if clf==0: return 0
    freqsum=sum([self.fprob(f,c) for c in self.categories()])
    p=clf/(freqsum)
    return p
	
  def fisherprob(self,item,cat):
    p=1
    features=self.getfeatures(item)
    for f in features:
      p*=(self.weightedprob(f,cat,self.cprob))
    fscore=-2*math.log(p)
    return self.invchi2(fscore,len(features)*2)	

def invchi2(self,chi, df):
    m = chi / 2.0
    sum = term = math.exp(-m)
    for i in range(1, df//2):
        term *= m / i
        sum += term
    return min(sum, 1.0)

  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.minimums={}

  def setminimum(self,cat,min):
    self.minimums[cat]=min
  
  def getminimum(self,cat):
    if cat not in self.minimums: return 0
    return self.minimums[cat]
  
  def classify(self,item,default=None):
    best=default
    max=0.0
    for c in self.categories():
      p=self.fisherprob(item,c)
      if p>self.getminimum(c) and p>max:
        best=c
        max=p
	print str(round(p,4))+"&"
	return best
	
def entryfeatures(entry):
  splitter=re.compile('\\W*')
  f={}
  
  titlewords=[s.lower() for s in splitter.split(entry['title']) 
          if len(s)>2 and len(s)<20]
  for w in titlewords: f['Title:'+w]=1

  summarywords=[s.lower() for s in splitter.split(entry['summary']) 
          if len(s)>2 and len(s)<20]

  uc=0
  for i in range(len(summarywords)):
    w=summarywords[i]
    f[w]=1
    if w.isupper(): uc+=1

    if i<len(summarywords)-1:
      twowords=' '.join(summarywords[i:i+1])
      f[twowords]=1
   
  return f	
  
def main():
  cl=classifier(getwords)
  cl.train('foreign, world, japan','international')
  cl.train('model, perfume, clothes','fashion')
  cl.train('award, nominated, nominee','awards')
  cl.train('tour, schedule, concert','shows')
  print cl.categories()
  f=feedparser.parse('feedlist.xml')
  i=0
  manul_entry={}
  manul_sumry={}
  second_fifty_entry={}
  for entry in f['entries'][0:100]:
   
   title=entry['title'].encode('utf-8')
   Sumry='%s\n%s' % (entry['title'],entry['summary'])

   i+=1
   Dic=getwords(Sumry)
   categ='international'
   I_total=0.0
   A_total=0.0
   F_total=0.0
   S_total=0.0
   for w in Dic:
    I_total+=cl.fcount(w,'international')
    A_total+=cl.fcount(w,'awards')
    F_total+=cl.fcount(w,'fashion')
    S_total+=cl.fcount(w,'shows')
   value = max(I_total,A_total,F_total,S_total)
   if value==F_total:
    categ='fashion'
   if value==S_total:
    categ='shows' 
   if value==A_total:
    categ='awards'
   if value==I_total:
    categ='international'
   manul_entry[title]=categ
   manul_sumry[title]=Sumry
   print str(i)+': '+title+"\t\t"+categ
   
  cl=fisherclassifier(getwords)
  for key,value in manul_sumry.iteritems():
    cl.train(key,manul_entry[key])
  
  for entry in f['entries'][50:100]:
   title=entry['title'].encode('utf-8')
   T_Sumry='%s\n%s' % (entry['title'],entry['summary'])
   i+=1
   print title+"&"
   predicat=str(cl.classify(T_Sumry))
   print predicat+"&"+manul_entry[title]+"\\\\"
   cl.train(T_Sumry,predicat)
   actual=manul_entry[title]
 
main();