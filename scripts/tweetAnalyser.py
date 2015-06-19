#usr/bin/python3.4

import sys
import nltk
from collections import Counter, namedtuple, defaultdict
import datetime
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
import time

def tweetFilter(tokens):
	""" Filters out hashtags, links and other irrelevant characters """
	newTokens = []
	for token in tokens:
		if not token.startswith('@'):
			if not token.startswith('http'):
				if not token.startswith('"'):
					if not token == 'RT':
						newTokens.append(token.lower())
	for i in range(len(newTokens)):
		for ch in newTokens[i]:
			if ch in ['!', '?', ',', '.', '(', ')', '#', '/', '\\', '|']:
				newTokens[i] = newTokens[i].replace(ch, "")
	return newTokens

def getData(infile, stopWordList):
	""" Gets the relevant data from the tweet for event detection """
	allwords = []
	timeList = []
	Tweet = namedtuple('Tweet', 'ID, TIME, TEXT, ANNO')
	for line in infile:
		twid, twtime, twtext, twanno = line.split('\t')
		tweet = Tweet(twid, twtime, twtext, twanno)
		if twanno[:-1] == '1':
			hour, minute, second = twtime.split(':')
			oldtokens = twtext.split()
			tokens = tweetFilter(oldtokens)
			minuteList = [hour + '.' + minute, ' '.join(tokens)]
			timeList.append(minuteList)
			bigrams = list(nltk.bigrams(tokens))
			trigrams = list(nltk.trigrams(tokens))
			for token in tokens:
				if token not in stopWordList:
					allwords.append(token)
	return timeList, allwords

def makePlayerLists(stopWordList):
	""" Creates playerlists for each team from file """
	homeplayerFile = open('../playerlists/australiaplayers.txt', 'r')
	awayplayerFile = open('../playerlists/netherlandsplayers.txt', 'r')
	homelistforDict = []
	awaylistforDict = []
	homeplayerList = []
	awayplayerList = []
	
	for line in homeplayerFile:
		homenames = line.split()
		homelistforDict.append(homenames)
		for homename in homenames:
			if homename not in stopWordList:
				homeplayerList.append(homename.lower())
	
	for line in awayplayerFile:
		names = line.split()
		awaylistforDict.append(names)
		for name in names:
			if name not in stopWordList:
				awayplayerList.append(name.lower())
	return homeplayerList, awayplayerList, homelistforDict, awaylistforDict

def checkTweetforPlayer(tweetlist, homeplayers, awayplayers):
	""" Checks the tweet for player mentions """
	checkList = []
	for tweet in tweetlist:
		splittweet = tweet.split()
		for word in splittweet:
			if word in homeplayers or word in awayplayers:
				checkList.append(word)
	c = Counter(checkList)
	for value, freq in c.most_common(1):
		return value

def checkTweetforEvent(tweetlist):
	""" Checks the tweet for different events """
	goaleventlist = 	['doelpunt', 'doelpuntje', 'goal', 'goaltje', 'prachtgoal',
				 		'wereldgoal','golazo', 'werelddoelpunt', 'assist', 'gollazo', 
				 		'supergoal', 'superdoelpunt']
	cardeventlist =		['rode', 'gele', 'rood', 'geel', 'kaart']
	checkList = []
	for tweet in tweetlist:
		splittweet = tweet.split()
		for word in splittweet:
			if word in goaleventlist:
				checkList.append('doelpunt')
			if word in cardeventlist:
				checkList.append('kaart')
	c = Counter(checkList)
	for value, freq in c.most_common(1):
		return value


def mathplot(clusters):
	""" Plot a graph with amount of tweets on the Y-axis and time on the X-axis """
	style.use('ggplot')

	x = []
	y = []
	for times, tweets in sorted(clusters.items()):
		oldtime = times
		minute, second = times.split('.')		
		second = float(second) / 60 * 100
		newtime = float(minute) + second / 100
		x.append(newtime)
		y.append(len(tweets))

	plt.plot(x,y)

	plt.title('Aantal tweets x Tijd')
	plt.ylabel('Aantal tweets')
	plt.xlabel('Tijd')

	plt.show()

def makeplayerDictbyList(homeplayers, awayplayers):
	""" Make dictionary based on playerlists for nicer output """
	playerDict = {}
	for line in homeplayers:
		playerDict[line[-1]] = ' '.join(line)
	for line in awayplayers:
		playerDict[line[-1]] = ' '.join(line)
	return playerDict


def main(argv):
	annotatedFile = open(argv[1], 'r', encoding='UTF-8')
	stopWordList = [word[:-1] for word in open('../stopwords.txt', 'r')]
	
	timeList, allwords = getData(annotatedFile, stopWordList)
	homeplayers, awayplayers, homelistforDict, awaylistforDict = makePlayerLists(stopWordList)
	playerDict = makeplayerDictbyList(homelistforDict, awaylistforDict)
	tweetclusters = defaultdict(list)

	for timestamp, tweet in timeList:
		tweetclusters[timestamp].append(tweet)

	#mathplot(tweetclusters)

	timetweetList = []
	for times, tweets in sorted(tweetclusters.items()):
		if len(tweets) > 10:
			player = checkTweetforPlayer(tweets, homeplayers, awayplayers)
			event = checkTweetforEvent(tweets)
			timetweetList.append((times, str(player).title(), str(event)))
	homeGoals = 0
	awayGoals = 0
	prevEventPlayer = ''
	for time, player, event in timetweetList:
		if (event, player) != prevEventPlayer:
			if event == 'kaart':
				print("{}\t{:<10}\t{}".format(time, event, playerDict[player]))
			else: #if event == 'doelpunt':
				if player.lower() in homeplayers:
					homeGoals += 1
				if player.lower() in awayplayers:
					awayGoals += 1
				print("{}\t{}-{:<10}\t{}".format(time, homeGoals, awayGoals, playerDict[player]))
		prevEventPlayer = (event, player)

	

if __name__ == '__main__':
	main(sys.argv)
