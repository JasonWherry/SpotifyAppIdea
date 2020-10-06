'''
Jason's Machine --> macOS Catalina 10.15.6 : Terminal CLI : GNU bash 3.2.57	

run with:	python3 compareUsers.py

Purpose:	Initialize SQLite DB (SpotifyData) with StreamingHistory.

			Compare & contrast the StreamingHistory files of 2 Users.

Goal:		gain insight into the preferences of the Users, together as a couple, and individually too. 

Methods:	1. load JSON objects into Panda/NumPy objects	2. create a DB with the JSON objects	3. Try both 1 & 2

Tech:		Python 3.7.5		SQLiteStudio 3.22.0		GNU bash 3.2.57		git 2.21.0

Done:		Store a User's Streaming History into a Table (StreamingHistory) 

To Do:		Create a User Table - define relationship with StreamingHistory Table; userID primary/foreign key
				This way, we can divide StreamingHistory Data by a userID. 
				Also, the User Table will hold Info about each person such as (userID, userName, email, firstName, lastName, creationTime, etc.)

'''

import json
import sqlite3
import glob

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
	c.execute('CREATE TABLE IF NOT EXISTS StreamingHistory(id integer primary key AUTOINCREMENT , fileID integer, endTime varchar(100), artistName varchar(100), trackName varchar(100), msPLayed varchar(100))')

	# folder = input('enter the path to your \'MyData\' folder: ')	# /Users/jasonwherry/Desktop/SpotifyAppIdea/jay_data/
	# files = glob.glob(folder+'StreamingHistory*.json')
	# print('loading these files into DB: ', *files, sep='\n')

	# for i in files:
	# print('filepath ', filePath)
	locNum = filePath.find('History')
	locDot = filePath.find('.')
	count = filePath[locNum+7:locDot]
	with open(filePath) as json_file:
		print('loading file ...', filePath, '\n')
		data = json.load(json_file)
		for obj in data:
			c.execute('insert into StreamingHistory (fileID, endTime, artistName, trackName, msPlayed) values (?, ?, ?, ?, ?)',
				[count, obj['endTime'], obj['artistName'], obj['trackName'], obj['msPlayed']])
			conn.commit()
	conn.close()


dropTable('SpotifyData.db', 'StreamingHistory')

loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/jay_data/StreamingHistory0.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/jay_data/StreamingHistory1.json')
loadDB('SpotifyData.db', '/Users/jasonwherry/Desktop/SpotifyAppIdea/jay_data/StreamingHistory2.json')

