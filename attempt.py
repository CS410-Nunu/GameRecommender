import sqlite3 as lite

def getCluster(games):
	con = None
	con = lite.connect('gameclusters.db')
	cur = con.cursor()
	recommendedList = []
	totalTimePlayed = 0
	print games
	for game in games[0:1]:
		totalTimePlayed += game[1]

	for game in games[0:1]:
		cur.execute("SELECT * FROM GameClusters WHERE gameID=?", (game[0], ))
		con.commit()

		row = cur.fetchone()
		cur.execute("SELECT gameID FROM GameClusters WHERE clusterID=?", (row[1], ))
		con.commit()

		clusterGames = cur.fetchall()

		con2 = lite.connect('gameinfo.db')
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
					players_2weeks = players_2weeks/players
					players = players/25000000.0 #Normalized by most popular game Dota
					#playtime_forever = gameInfo['playtime_forever']
					playtime_2weeks = playtime_2weeks/1799.0
					#print timePlayedNormalized
					recommendedList.append((clustergame[0], timePlayedNormalized + players +
						players_2weeks + playtime_2weeks))
		con2.close()

	con.close()

	#print recommendedList
	#print recommendedList
	recommendedList.sort(key=lambda x: x[1], reverse=True)
	return recommendedList


def getInfo(recommendedList):
	con = lite.connect('appInfo.db')
	cur = con.cursor()

	mylist = []

	for item in recommendedList[0:10]:
		cur.execute("SELECT * FROM AppInfo WHERE gameID=?", (item[0],))
		con.commit()
		gameInfo = cur.fetchone()
		mylist.append(gameInfo)

	return mylist

result = getInfo(getCluster([(278910, 100)]))

for res in result:
	print res[2]






