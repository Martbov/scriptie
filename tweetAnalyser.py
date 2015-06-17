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
	homeplayerFile = open('australiaplayers.txt', 'r')
	awayplayerFile = open('netherlandsplayers.txt', 'r')
	homeplayerList = []
	awayplayerList = []
	
	for line in homeplayerFile:
		homenames = line.split()
		for homename in homenames:
			if homename not in stopWordList:
				homeplayerList.append(homename.lower())
	
	for line in awayplayerFile:
		names = line.split()
		for name in names:
			if name not in stopWordList:
				awayplayerList.append(name.lower())
	return homeplayerList, awayplayerList

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

def makePlayerDict():
	playerdict = {
	'Blind' : 'Daley Blind',
	'Cillessen' : 'Jasper Cillessen',
	'Clasie' : 'Jordy Clasie',
	'Depay' : 'Memphis Depay',
	'Fer' : 'Leroy Fer',
	'Guzman' : 'Jonathan de Guzman',
	'Huntelaar' : 'Klaas Jan Huntelaar',
	'Janmaat' : 'Daryl Janmaat',
	'Jong' : 'Nigel de Jong',
	'Kongolo' : 'Terence Kongolo',
	'Krul' : 'Tim Krul',
	'Kuyt' : 'Dirk Kuyt',
	'Lens' : 'Jeremain Lens',
	'Indi' : 'Bruno Martins Indi',
	'Persie' : 'Robin van Persie',
	'Robben' : 'Arjen Robben',
	'Sneijder' : 'Wesley Sneijer',
	'Veltman' : 'Joël Veltman',
	'Verhaegh' : 'Paul Verhaegh',
	'Vlaar' : 'Ron Vlaar',
	'Vorm' : 'Michel Vorm',
	'Vrij' : 'Stefan de Vrij',
	'Wijnaldum' : 'Georginio Wijnaldum',
	'Casillas' : 'Iker Casillas',
	'Azplicueta' : 'Cesar Azplicueta Tanco',
	'Piqué' : 'Gerard Piqué',
	'Alba' : 'Jordi Alba Ramos',
	'Ramos' : 'Sergio Ramos García',
	'Iniesta' : 'Andrés Iniesta',
	'Silva' : 'David Silva',
	'Fabregas' : 'Francesc Fabregas',
	'Busquets' : 'Sergio Busquets',
	'Alonso' : 'Xabier Alonso',
	'Pedro' : 'Pedro Rodriquez Ledesma',
	'Xavi' : 'Xavier Hernández Creus',
	'Costa' : 'Diego Costa',
	'Torres' : 'Fernando Jose Torres Sanz',
	'Ryan' : 'Mathew Ryan',
	'Wilkinson' : 'Alex Wilkinson',
	'Davidson' : 'Jason Davidson',
	'Spiranovic' : 'Mattew Spiranovic',
	'McGowan' : 'Ryan McGowan',
	'Bresciano' : 'Marc Bresciano',
	'Dgani' : 'Orel Dgani',
	'Leckie' : 'Mathew Leckie',
	'Mckay' : 'Matt Mckay',
	'Jedinak' : 'Mile Jedinak',
	'Cahill' : 'Tim Cahill',
	'Halloran' : 'Ben Halloran',
	'Oar' : 'Adam Taggart'
	}
	return playerdict

def main(argv):
	annotatedFile = open(argv[1], 'r', encoding='UTF-8')
	stopWordList = [word[:-1] for word in open('stopwords.txt', 'r')]
	
	timeList, allwords = getData(annotatedFile, stopWordList)
	homeplayers, awayplayers = makePlayerLists(stopWordList)
	playerDict = makePlayerDict()
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
