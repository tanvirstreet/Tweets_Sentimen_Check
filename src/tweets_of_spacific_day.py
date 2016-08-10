
#!/usr/bin/env python
# encoding: utf-8
import pandas as pd
from datetime import datetime
import csv

# MonDay = 0
# TueDay = 1
# WedDay = 2
# TheDay = 3
# FriDay = 4
# SatDay = 5
# SunDay = 6

def get_date_tweets(username):
	myList = []
	with open('../data/tweets/%s_.csv' % (username), 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)

	for x in your_list:
		date = x[1]
		dateOb = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
		print(dateOb.weekday())
		# Set the day value in the if condition as Integer
		if dateOb.weekday()==4:
			myList.append([x[0],x[1],'Friday',x[2]])
			pass
	
	csvdataframe=pd.DataFrame(myList,columns=['twitter_id','date','day','tweet'])
	# Create a csv file with the Sentiment Polarity..
	csvdataframe.to_csv("../data/spDay/%s_.csv"%(username),index=False)
	
	pass

if __name__ == '__main__':
	# Pass in the username of the account you want to download
	# This Username Must be the @username used in Twitter
	username = input("Enter the UserName: ")
	get_date_tweets(username)
	
# %Y-%m-%d %H:%M:%S
# %d-%m-%Y %H:%M:%S
# %m-%d-%Y %H:%M:%
# %d-%m-%y %H:%M