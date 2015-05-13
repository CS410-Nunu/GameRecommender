import sqlite3 as lite
import urllib, urllib2
import sys
import requests
import json

con = None

con = lite.connect('../gameclusters.db')

cur = con.cursor()
cur.execute("SELECT * FROM GameClusters")

rows = cur.fetchall()

cur.execute("DROP TABLE IF EXISTS GameInfo")
cur.execute("CREATE TABLE GameInfo(gameID TEXT, players INT, players_2weeks INT, playtime_forever INT, playtime_2weeks INT)")

i = 0

for row in rows:
	i += 1
	if i % 10 == 0:
		print 'Finished ' + str(i)
	appId = row[0]
	clusterId = row[1]

	try:
		url = "http://steamspy.com/api.php?request=appdetails&appid="
		data = json.loads(requests.get(url+row[0]).text)
		updateData = (
		 data['appid'],
		 data['players_forever'],
		 data['players_2weeks'],
		 data['average_forever'],
		 data['average_2weeks']
		)
		cur.execute("INSERT INTO GameInfo VALUES(?, ?, ?, ?, ?)", updateData)
	except :
		print 'Doesnt exist: ' + str(appId)
		cur.execute("INSERT INTO GameInfo VALUES(?, ?, ?, ?, ?)", (appId, 0 , 0, 0, 0))

con.commit()
con = con.close()