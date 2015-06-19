#!usr/bin/python3.4

import sys
import nltk
from collections import Counter

def tweetFilter(tokens):
	newTokens = []
	for token in tokens:
		if not token.startswith('@'):
			if not token.startswith('http'):
				if not token.startswith('"'):
					if not token == 'RT':
						newTokens.append(token.lower())
	for i in range(len(newTokens)):
		for ch in newTokens[i]:
			if ch in ['!', '?', ',', '.', '(', ')', '#', '/', '\\']:
				newTokens[i] = newTokens[i].replace(ch, "")
	return newTokens
		
def goaleventfeatures(tokens):
	relevantWords = ['doelpunt', 'doelpuntje', 'goal', 'goaltje', 'prachtgoal', 'wereldgoal','golazo', 'werelddoelpunt', 'assist', 'gollazo', 'supergoal', 'superdoelpunt']
	x = ""
	while x == "":
		for token in tokens:
			if token.lower() in relevantWords:
				return 1
				x = 'stop'
			else:
				continue
		return 0
		x = 'stop'

def cardeventfeatures(tokens):
	relevantWords = ['rode', 'gele', 'rood', 'geel', 'kaart']
	x = ""
	while x == "":
		for token in tokens:
			if token.lower() in relevantWords:
				return 1
				x = 'stop'
			else:
				continue
		return 0
		x = 'stop'

def playerfeatures(tokens):
	rawlist = []
	textlist = open('playerlist.txt', 'r')
	for line in textlist:
		names = line.split()
		for name in names:
			rawlist.append(name)
	playerlist = [player.lower() for player in rawlist]
	
	x = ""
	while x == "":
		for token in tokens:
			if token.lower() in playerlist:
				return 1
				x = 'stop'
			else:
				continue
		return 0
		x = 'stop'

def almostFilter(tokens):
	wordList = ['bijna','niet','mis','gemist','kans', 'falen', 'faalt', 'gefaald', 'jaar', 'geleden']
	x = ""
	while x == "":
		for token in tokens:
			if token.lower() in wordList:
				return 1
				x = 'stop'
			else:
				continue
		return 0
		x = 'stop'

def length(tokens):
	return(len(tokens))

def positiveWords(tokens):
	relevantWords = ['mooi', 'mooie', 'geweldig', 'geweldige', 'prachtig', 'prachtige', 'schoon', 'schone', 'heerlijke', 'heerlijk', 'schitterend', 'schitterende', 'awesome']
	x = ""
	while x == "":
		for token in tokens:
			if token.lower() in relevantWords:
				return 1
				x = 'stop'
			else:
				continue
		return 0
		x = 'stop'

def refereewWords(tokens):
	refWords = ['scheids', 'scheidsrechter', 'beslissing', 'fluit']
	x = ""
	while x == "":
		for token in tokens:
			if token.lower() in refWords:
				return 1
				x = 'stop'
			else:
				continue
		return 0
		x = 'stop'

def curseWords(tokens):
	curseWords = ['gvd', 'godverdomme', 'kut', 'kk', 'kanker']
	x = ""
	while x == "":
		for token in tokens:
			if token.lower() in curseWords:
				return 1
				x = 'stop'
			else:
				continue
		return 0
		x = 'stop'

def main(argv):
	print("@RELATION relevance")
	print()
	print("@ATTRIBUTE goalevent NUMERIC")
	print("@ATTRIBUTE cardevent NUMERIC")
	print("@ATTRIBUTE player NUMERIC")
	print("@ATTRIBUTE almost NUMERIC")
	print("@ATTRIBUTE length NUMERIC")
	print("@ATTRIBUTE positive NUMERIC")
	print("@ATTRIBUTE referee NUMERIC")
	print("@ATTRIBUTE cursewords NUMERIC")
	print("@ATTRIBUTE class 	{irrelevant, relevant}")
	print()
	print("@DATA")
	annotatedfile = open(argv[1], 'r')
	wordSet = set()
	for line in annotatedfile:
		twid, twtime, twtext, twanno = line.split('\t')
		tokens = twtext.split()
		newTokens = tweetFilter(tokens)

		#print(newTokens)
		vector = []
		vector.append(str(goaleventfeatures(newTokens)))
		vector.append(str(cardeventfeatures(newTokens)))
		vector.append(str(playerfeatures(newTokens)))
		vector.append(str(almostFilter(newTokens)))
		vector.append(str(length(newTokens)))
		vector.append(str(positiveWords(newTokens)))
		vector.append(str(refereewWords(newTokens)))
		vector.append(str(curseWords(newTokens)))
		#vector.append('?')
		if twanno[:-1] == '0':
			vector.append('irrelevant')
		else:
			vector.append('relevant')
		print(','.join(vector))

		
if __name__ == '__main__':
	main(sys.argv)