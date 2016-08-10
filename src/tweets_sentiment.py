#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import pandas as pd
import csv
from textblob import TextBlob

#Twitter API credentials
access_key = "695651038150266881-2iHmfIpodOhBCaxYndeFmQIucLouFRX"
access_secret = "SnZDYgPygKGdb8lqhPDgnIAhAIFpCUkZaSGtms7G8h1tP"
consumer_key = "jRPB3DWHBBEIiMNGTrywRN0UL"
consumer_secret = "iHHrFseYF5BEEByiRsQXhOQjqTC3teDNTZ2r8CIERmWUpFXLND"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	dataframe=pd.DataFrame(outtweets,columns=['twitter_id','date','tweet'])
	# Creating a csv file which contain the Tweets as per the Data.
	dataframe.to_csv("../data/tweets/%s_.csv"%(screen_name),index=False)
	
	return

def sentimentCheck(text):
	blob = TextBlob(text)
	blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
	                    #  ('threat', 'NN'), ('of', 'IN'), ...]

	blob.noun_phrases   # WordList(['titular threat', 'blob',
	                    #            'ultimate movie monster',
	                    #            'amoeba-like mass', ...])
	lineCount=0
	totalPolarity = 0.0
	s=""
	for sentence in blob.sentences:
	    lineCount+=1
	    totalPolarity += sentence.sentiment.polarity
	    s+=str(sentence.sentiment.polarity) + ","

	blob.translate(to="es")
	polarityPoints = s[:-1]
	avaragePolarity = totalPolarity / lineCount

	return polarityPoints, avaragePolarity

def save_sentiment_polarities(username):
	myList = []
	with open('../data/tweets/%s_.csv' % (username), 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)

	for x in your_list:
		tex = x[2]
		pp, ap = sentimentCheck(tex)
		myList.append([x[0],x[1],tex, pp , ap])

	csvdataframe=pd.DataFrame(myList,columns=['twitter_id','date','tweet','polarityPoints','avaragePolarity'])
	# Create a csv file with the Sentiment Polarity..
	csvdataframe.to_csv("../data/emo/%s_.csv"%(username),index=False)
	
	pass

if __name__ == '__main__':
	# Pass in the username of the account you want to download
	# This Username Must be the @username used in Twitter
	username = input("Enter the UserName: ")
	get_all_tweets(username)
	#This mathod create the CSV file with the Sentiment Properties
	save_sentiment_polarities(username)

