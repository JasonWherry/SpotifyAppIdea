'''
Jason's Machine --> macOS Catalina 10.15.6 : Terminal CLI : GNU bash 3.2.57	

run with:	python3 compareUsers.py

Purpose:	Initialize SQLite DB (SpotifyData) with StreamingHistory.

			Compare & contrast the StreamingHistory files of 2 Users.

Goal:		gain insight into the preferences of the Users, together as a couple, and individually too. 

Methods:	1. load JSON objects into Panda/NumPy objects	2. create a DB with the JSON objects	3. Try both 1 & 2

Tech:		Python 3.7.5		SQLiteStudio 3.22.0		GNU bash 3.2.57		git 2.21.0

Done:		Store a User's Streaming History into a Table (StreamingHistory) 

			Create a User Table - define relationship with StreamingHistory Table; userID primary/foreign key
				-- find the tracks that the Users have in common. 
				-- going to need two separate tables for the users, then join them and see where user1.trackName = user2.trackName
				
				select distinct * from Users as user1 JOIN Users as user2 where user1.userid != user2.userid and user1.tracks = user2.tracks;

To Do:		restructure DataBase design
			optomize database entry. Is 'insert into <table>' the best way to add data to SQLite3DB through Python?

'''

import json
import sqlite3
import glob

def createTables(DBName):
	conn = None
	try:
		conn = sqlite3.connect(DBName)	# 'StreamingHistory.db'

	except sqlite3.Error as er:
		print(er)

	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS StreamingHistory(id integer primary key AUTOINCREMENT , user integer, fileID integer, endTime varchar(100), artistName varchar(100), trackName varchar(100), msPLayed varchar(100))')

	c.execute('CREATE TABLE IF NOT EXISTS Users(userid integer, tracks varchar(100), foreign key(userid) references StreamingHistory(user))')

	conn.commit()
	conn.close()

def addUser(DBName, userNum):
	conn = None
	try:
		conn = sqlite3.connect(DBName)	# 'StreamingHistory.db'

	except sqlite3.Error as er:
		print(er)

	c = conn.cursor()
	c.execute('select COUNT(id) as total from StreamingHistory where user = {}'.format(userNum) )
	result = c.fetchone()
	trackCount = result[0]
	print('trackCount: ',trackCount)
	c.execute('insert into Users (userid, tracks) values(?, ?)', [userNum, trackCount])	
	conn.commit()
	conn.close()

def dropTable(DBName, tableName):
	conn = sqlite3.connect(DBName)
	c = conn.cursor()
	c.execute('DROP TABLE IF EXISTS '+ tableName)
	conn.commit()
	conn.close()

'''
Creates a DB and loads StreamingHistory (JSON files)
'''
def loadDB(DBName, filePath):
	conn = None
	try:
		conn = sqlite3.connect(DBName)	# 'StreamingHistory.db'

	except sqlite3.Error as er:
		print(er)

	c = conn.cursor()

	locNum = filePath.find('History')
	locDot = filePath.find('.')
	count = filePath[locNum+7:locDot]
	with open(filePath) as json_file:
		print('loading file ...', filePath, '\n')
		data = json.load(json_file)
		for obj in data:
			c.execute('insert into StreamingHistory (user, fileID, endTime, artistName, trackName, msPlayed) values (?, ?, ?, ?, ?, ?)',
				[userNum, count, obj['endTime'], obj['artistName'], obj['trackName'], obj['msPlayed']])
			c.execute('insert into Users (userid, tracks) values(?, ?)',
				[userNum, obj['trackName']])
			conn.commit()
	conn.close()

dropTable('SpotifyData.db', 'StreamingHistory')
dropTable('SpotifyData.db', 'Users')


createTables('SpotifyData.db')

# first user
userNum = 1	# stores userid
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/jay_data/StreamingHistory0.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/jay_data/StreamingHistory1.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/jay_data/StreamingHistory2.json')

# addUser('SpotifyData.db', userNum)

# second user
userNum += 1
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/noah_data/StreamingHistory0.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/noah_data/StreamingHistory1.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/noah_data/StreamingHistory2.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/noah_data/StreamingHistory3.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/noah_data/StreamingHistory4.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/noah_data/StreamingHistory5.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/noah_data/StreamingHistory6.json')


# addUser('SpotifyData.db', userNum)
