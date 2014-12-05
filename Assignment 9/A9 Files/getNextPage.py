#!/usr/bin/python3
import BeautifulSoup
import requests
import os, sys


def listOfPageFeedsPageCount(blog):

	feedPages = []
	if( len(blog) > 0 ):

		if( blog[len(blog)-1] != '/' ):
			blog = blog + '/feeds/posts/default/'
		else:
			blog = blog + 'feeds/posts/default/'
		
		listOfPageFeeds = paginate(blog, feedPages)

	
	return listOfPageFeeds

def paginate(blog, listOfPages=[]):

	html = requests.get(blog)
	link = BeautifulSoup(html.text).find('link', { 'rel' : 'next' })

	if link is not None:
		link = link['href']
		listOfPages.append(link)

		paginate(link, listOfPages)
	
	return listOfPages
out = open('numberOfPages.txt', 'a')

with open("feedlist.txt", "r") as f:
  for line in f:
	url = line.strip()

	arrayOfPages = listOfPageFeedsPageCount(url)
	Number = len(arrayOfPages) + 1
	print Number
	out.write(str(Number))
	out.write('\n') 
	for page in arrayOfPages:
		print page
out.close()