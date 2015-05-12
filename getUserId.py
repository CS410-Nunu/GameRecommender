import httplib
import urllib, urllib2
from bs4 import BeautifulSoup

def getUserId(username):
	data = {'input' : username}
	data = urllib.urlencode(data)
	req = urllib2.Request('https://steamid.io/lookup ', data) 
	response = urllib2.urlopen(req)
	the_page = response.read()
	soup=BeautifulSoup(the_page)
	notFound = soup.find("p", {"class": "notice alert-danger"}).text.strip()
	if notFound == "profile not found":
		# not found
		return -1 
	else:
		href = soup.find("h4", {"class": "media-heading"}).findNext("a")['href']
		req = urllib2.Request(href)
		response = urllib2.urlopen(req)
		soup = BeautifulSoup(response.read())
		steamid64 = soup.find("dt", text="steamID64").findNext("dd").contents[0]
		return steamid64
	
#print getUserId("jsakdjfksajdfjs")
#print getUserId("grimorder27")
#print getUserId("sonicace22")