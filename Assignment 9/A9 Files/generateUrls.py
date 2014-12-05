#!/usr/bin/python3
import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse

DEFAULT_COUNT=98
DEFAULT_SEED_URL='http://www.blogger.com/next-blog?navBar=true&blogID=3471633091411211117'
if len(sys.argv) != 3:
    print('Pass the blog count, defaulting to ' + str(DEFAULT_COUNT))
    print('Pass the seed URL, defaulting to ' + DEFAULT_SEED_URL)
    count=DEFAULT_COUNT
    url=DEFAULT_SEED_URL
else:
    count=sys.argv[1]
    url=sys.argv[2]

def parse(link):
    response = urllib.request.urlopen(link)
    soup = BeautifulSoup(response.read())
    response.close()
    return soup

def addNext(url,s):
    try:
        soup=parse(url)
        for atom in soup.findAll('link',rel='alternate',type='application/atom+xml'):
            atomHref=str(atom['href']).strip()
            s.add(atomHref)
            print('Added atom href: ' + atomHref)
    except:
        print('Exception parsing URL, skipping to next')
        pass

s=set()
while len(s) < count:
    addNext(url,s)
with open('feedlist.txt', 'w') as f:
    for atom in s:
        f.write(atom + '\n')
