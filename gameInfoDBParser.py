import sqlite3 as lite
import json

data = json.loads(open('gameInfo.json').read())

con = None

con = lite.connect('appinfo.db')

cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS AppInfo")
cur.execute("CREATE TABLE AppInfo(gameID TEXT, description TEXT, name TEXT, user_reviews TEXT)")

i = 0

for item in data:
	i += 1
	if i % 20 == 0:
		print 'Finished ' + str(i)
	cur.execute("INSERT INTO AppInfo VALUES(?, ?, ?, ?)", (item['appid'], item['about'], 
		item['name'], item['user_reviews']))

con.commit()