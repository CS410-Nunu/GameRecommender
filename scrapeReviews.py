from bs4 import BeautifulSoup
import mechanize
import json
import requests
from nltk.corpus import stopwords
import string
import os
#	Run this file with python2
# 	in mechanize dir run python setup.py install
hdr = {'User-Agent': 'Mozilla/5.0'}
cachedStopWords = stopwords.words("english")
print cachedStopWords
punctuation = string.punctuation
table = string.maketrans("", "")
br = mechanize.Browser()
br.addheaders = [('User-Agent', 'Firefox')]

def removeStopWords(text):
	removedText = ' '.join([word for word in text.split() if word not in cachedStopWords])
	return removedText.translate(table, punctuation)

def allGameReviews():
	br.open("http://store.steampowered.com/agecheck/app/" + str(10) + '/')
	br.select_form(nr=1)
	br.form['ageDay'] = ["1"]
	br.form['ageMonth'] = ["January"]
	br.form['ageYear'] = ["1900"]
	br.submit()
	json_data = open('validGames.json')
	data = json.load(json_data)
	json_data.close()
	gameInfoFile = open('gameInfo.json', 'w+')
	i = 1
	for d in data:
		if i % 10 == 0:
			print "added " + str(i)
		gameName, user_reviews, release_date, tags, about, reviews = getGameInfo(d["appid"])
		json.dump({'name': gameName, 'appid': d["appid"], 'user_reviews': user_reviews, 'release_date': release_date, 'tags': tags, 'about': about}, gameInfoFile, sort_keys = True, indent = 4, ensure_ascii=False)
		r_file = open(os.path.join('reviews', str(d["appid"])), 'w')
		for r in reviews:
			r_file.write(r + '\n')
		r_file.close()
		i += 1
	gameInfoFile.close()

def getGameInfo(appid):
	try: 
		br.open("http://store.steampowered.com/agecheck/app/" + str(appid) + '/', timeout = 240.0)
		soup = BeautifulSoup(br.response().read())
		gameName = ""
		gName = soup.find('div', 'apphub_AppName')
		if gName != None:
			gameName = gName.text.strip().encode('ascii', 'ignore')
		print "Adding " + gameName
		metaLink = soup.find("div", {"id": "game_area_metalink"})
		metaURL = ""
		if metaLink != None and metaLink.text != "Not yet reviewed.":
			metaURL = metaLink.findAll("a", {"href": True})[0]['href']
		d = soup.find(id='Reviews_all')
		#	negative, mixed, overwhelmingly positive
		user_reviews = ""
		ur = soup.find('span', 'game_review_summary')
		if ur != None:
			user_reviews = ur.text.strip().encode('ascii', 'ignore')
		release_date = ""
		rdate = soup.find('span', 'date')
		if rdate != None:
			release_date = rdate.text
		tHTML = soup.find('div', 'glance_tags popular_tags')
		tags = []
		if tHTML != None:
			for t in tHTML.findAll("a", {"href": True}):
				tags.append(t.text.strip().encode('ascii', 'ignore'))
		about = ""
		a_text = soup.find('div', {'id': 'game_area_description', 'class': 'game_area_description'})
		if a_text != None:
			about = a_text.text.strip().encode('ascii', 'ignore')[15:]
		
		reviews = []
		review_divs = []
		if d != None:
			for div in d.find_all('div', recursive=False):
				r_div = div.find_all('div', 'review_box')
				review_divs.extend(r_div)
			for div in review_divs:
				r = div.find('div', 'content').text.strip().encode('ascii', 'ignore')
				reviews.append(removeStopWords(r.lower()))
		if metaURL != "":
			metaReviews = getMetacriticReviews(metaURL)
			reviews.extend(metaReviews)
		return gameName, user_reviews, release_date, tags, about, reviews
	except (mechanize.HTTPError, mechanize.URLError):
		print "error for " + str(appid)
		return "", "", "", [], "", []

def getMetacriticReviews(url):
	print "Getting metacritic reviews"
	reviewUrl = url + "/user-reviews?sort-by=most-helpful&num_items=100"
	response = requests.get(reviewUrl, headers=hdr, timeout=60.0)
	soup = BeautifulSoup(response.text)
	divs = soup.find_all('div', {"class": "review_body"})
	reviews = []
	for d in divs:
		removedWords = removeStopWords(d.text.strip().encode('ascii', 'ignore').lower())
		reviews.append(removedWords)
	return reviews

def checkActualGame(data):
	br = mechanize.Browser()
	br.addheaders = [('User-Agent', 'Firefox')]
	count = 0
	jsonFile = open('validGames.json', 'w+')
	for i in data: 
		#appidStr = i["appid"].encode('ascii', 'ignore')
		print "on " + i["name"]
		try: 
			br.open("http://store.steampowered.com/agecheck/app/" + str(i["appid"]) + '/', timeout=60.0)
			invalid_title = "Welcome to Steam"
			if br.title() != invalid_title:
				if i["appid"] == 10:
					br.select_form(nr=1)
					br.form['ageDay'] = ["1"]
					br.form['ageMonth'] = ["January"]
					br.form['ageYear'] = ["1900"]
					br.submit()
				expectedUrl = "http://store.steampowered.com/app/" + str(i["appid"]) + "/"
				try:
					soup = BeautifulSoup(br.response().read())
					about = soup.find('div', {'id': 'game_area_description', 'class': 'game_area_description'})
					if about != None and about.text.strip().encode('ascii', 'ignore')[:15] == "About This Game" and expectedUrl == br.geturl():
						json.dump({'name': i["name"].encode('ascii', 'ignore').decode('ascii'), 'appid': i["appid"]}, jsonFile, sort_keys = True, indent = 4, ensure_ascii=False)
						print "added " + i["name"]
						count += 1
				except httplib.IncompleteRead:
					print "incomplete read"
		except (mechanize.HTTPError, mechanize.URLError):
			print "error for " + i["name"]
	jsonFile.close()
	print "done"
	print(count)

def parse_data(fileName = 'applist.json'):
        json_data = open(fileName)
        data = json.load(json_data)
        json_data.close()
        return data["applist"]["apps"]

#removeStopWords()
#allGameReviews()
#getGameInfo(2420)
#getMetacriticReviews("http://www.metacritic.com/game/pc/counter-strike-source")
#getGame(257350)
