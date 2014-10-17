#Mechanize and Beautiful soup can't inteface with the javascript used for the infinite scroll: I was able to login, see friends but not able
#to scroll to see more friends

#pip install -U selenium
#sources:
#https://gist.github.com/leostera/3535568
#https://pypi.python.org/pypi/selenium
#cookies problem: http://stackoverflow.com/questions/7854077/using-a-session-cookie-from-selenium-in-urllib2

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import os, sys

#dirty code, consider user behaviour simulation, not found exceptions, etc
#output file: allFacebookFriends.html
def getHtmlOfAllFriends(userFaceBookEmail, userFaceBookPassword, LastFriendName):

	if( len(userFaceBookEmail) > 0 and len(userFaceBookPassword) > 0 and len(LastFriendName) > 0 ):
		pass
	else:
		print "one input length is bad"
		return

	try:
		htmlOutputFile = open('allFacebookFriends.html', 'w')
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print fname, exc_tb.tb_lineno, sys.exc_info()
		return

	myFirefoxBrowser = webdriver.Firefox()
	myFirefoxBrowser.implicitly_wait(3)
	# or you can use Chrome(executable_path="/usr/bin/chromedriver")
	myFirefoxBrowser.get("http://www.facebook.org")
	assert "Facebook" in myFirefoxBrowser.title


	elem = myFirefoxBrowser.find_element_by_id("email")
	elem.send_keys(userFaceBookEmail)
	elem = myFirefoxBrowser.find_element_by_id("pass")
	elem.send_keys(userFaceBookPassword)
	elem.send_keys(Keys.RETURN)

	#http://stackoverflow.com/questions/7854077/using-a-session-cookie-from-selenium-in-urllib2
	all_cookies = myFirefoxBrowser.get_cookies()
	#cookies = {}
	#for s_cookie in all_cookies:
	#    cookies[s_cookie["name"]]=s_cookie["value"]


	#open friends page
	friendsLink = 'https://www.facebook.com/friends/'
	myFirefoxBrowser.get(friendsLink)
	myFirefoxBrowser.maximize_window()


	#scroll to bottom of page
	for i in range(0, 20):
		myFirefoxBrowser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		html = myFirefoxBrowser.page_source.encode('utf-8') 
		

		if( html.find(LastFriendName) > -1 ):
			htmlOutputFile.write(html)
			print "found"
			break

		time.sleep(5)


	myFirefoxBrowser.close()


usr = ''
pwd = ''
lastFriendName = ''
getHtmlOfAllFriends(usr, pwd, lastFriendName)
