from flask import Flask, render_template, request, redirect, url_for
import os
import sys
sys.path.append("../")
from SteamUser import SteamUser
import sqlite3 as lite
import json

def getRatingValue(gameInfo):
	rating = gameInfo[3]
	value = 0
	if rating == 'Overwhelmingly Positive':
		value = 9
	elif rating == 'Very Positive':
		value = 8
	elif rating == 'Positive':
		value = 7
	elif rating == 'Mostly Positive':
		value = 6
	elif rating == 'Mixed':
		value = 5
	elif rating == 'Mostly Negative':
		value = 4
	elif rating == 'Negative':
		value = 3
	elif rating == 'Very Negative':
		value = 2
	elif rating == 'Overwhelmingly Negative':
		value = 1
	else:
		value = 0
	return value/9.0

def checkInGames(myid, games):
	for game in games[0:10]:
		if game[0] == myid:
			return True

	return False

def checkInClusters(myid, games):
	for game in games:
		if game == myid:
			return True

	return False

def getCluster(games):
	con = None
	con = lite.connect('../gameclusters.db')
	cur = con.cursor()
	recommendedList = []
	totalTimePlayed = 0
	for game in games[0:10]:
		totalTimePlayed += game[1]

	con3 = lite.connect('../appInfo.db')
	cur3 = con3.cursor()

	clustersAdded = []

	for game in games[0:10]:
		cur.execute("SELECT * FROM GameClusters WHERE gameID=?", (game[0], ))
		con.commit()

		row = cur.fetchone()

		if row is None:
			print game[0]
			continue

		if checkInClusters(row[1], clustersAdded) is True:
			continue

		clustersAdded.append(row[1])
		cur.execute("SELECT gameID FROM GameClusters WHERE clusterID=?", (row[1], ))
		con.commit()

		clusterGames = cur.fetchall()

		con2 = lite.connect('../gameinfo.db')
		cur2 = con2.cursor()

		for clustergame in clusterGames:
			timePlayedNormalized = game[1]/float(totalTimePlayed) #Normalized
			
			cur2.execute("SELECT * FROM GameInfo WHERE gameID=?", (clustergame[0], ))
			con2.commit()
			gameInfo = cur2.fetchone()

			if gameInfo is None:
				temp = 1
				#recommendedList.append((clustergame[0], timePlayedNormalized * 4))
			else:
				gameid, players, players_2weeks, playtime_forever, playtime_2weeks = gameInfo
				if players == 0:
					temp = 1
					#recommendedList.append((clustergame[0], timePlayedNormalized * 4))
				else:
					cur3.execute("SELECT * FROM AppInfo WHERE gameID=?", (clustergame[0],))
					con3.commit()
					gameInfo = cur3.fetchone()
					rating = getRatingValue(gameInfo)
					if rating == 0:
						temp = 1
					else:
						players_2weeks = players_2weeks/float(players)
						players = players/25000000.0 #Normalized by most popular game Dota
						playtime_2weeks = playtime_2weeks/float(playtime_forever)
						#print timePlayedNormalized
						#recommendedList.append((clustergame[0],  timePlayedNormalized + players +
							#players_2weeks + playtime_2weeks + rating))
						if checkInGames(clustergame[0], games) == True:
							temp = 1
						else:
							recommendedList.append((clustergame[0], timePlayedNormalized + rating))
		con2.close()
    	con3.close()
	con.close()

	#print recommendedList
	#print recommendedList
	recommendedList.sort(key=lambda x: x[1], reverse=True)
	return recommendedList


def getInfo(recommendedList):
	con = lite.connect('../appInfo.db')
	cur = con.cursor()

	mylist = []

	for item in recommendedList[0:15]:
		cur.execute("SELECT * FROM AppInfo WHERE gameID=?", (item[0],))
		con.commit()
		gameInfo = cur.fetchone()
		mylist.append(gameInfo)
		print item[0]
		print gameInfo[2]
		print item[1]
		print '------------------------------------'

	return mylist


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/')
app = Flask(__name__, template_folder = tmpl_dir)

@app.route('/')
def login(games=None):
	#if redirect is True:
	return render_template('main.html', games=games)
	#else:
		#return render_template('main.html', games=games)

@app.route('/recommend', methods=['POST'])
def recommend(userId=None):
	#print request.form["userId"]
	info = SteamUser(request.form["userId"])
	try:
		games = info.getUserGames()
	except ID_NOT_FOUND_EXCEPTION as e:
		return 'Could Not Find User'

	#print games
	return render_template('main.html', games=getInfo(getCluster(games)))
	#return redirect(url_for('login', games=getInfo(getCluster(games))))

if  __name__ == '__main__':
	app.run(debug=True)