#!usr/bin/python3.4

import sys
import nltk

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
		
def eventfeatures(tokens):
	relevantWords = ['doelpunt', 'goal', 'rode', 'gele', 'rood', 'geel', 'kaart']
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
	homePlayers = [	'iker', 'casillas',
					'cesar', 'azpilicueta', 'tanco',
					'gerard', 'piqué',
					'jordi', 'alba', 'ramos',
					'sergio', 'ramos', 'garcía',
					'andrés', 'iniesta',
					'david', 'silva',
					'francesc', 'fabregas',
					'sergio', 'busquets',
					'xabier', 'alonso',
					'Pedro', 'rodriguez', 'Ledesma',
					'Xavier', 'Hernández', 'Creus',
					'Diego', 'Costa', 
					'Fernando', 'Jose', 'Torres', 'Sanz']
	awayPlayers = [	'Jasper', 'Cillessen',
					'Bruno', 'Martins', 'Indi',
					'Daryl', 'Janmaat',
					'Ron', 'Vlaar',
					'Stefan', 'De', 'Vrij',
					'Joël', 'Veltman',
					'Arjen', 'Robben',
					'Daley', 'Blind',
					'Jonathan', 'de', 'Guzman',
					'Georginio', 'Wijnaldum',
					'Nigel', 'de', 'Jong',
					'Wesley', 'Sneijder',
					'Robin', 'van', 'Persie', 'vanpersie'
					'Jeremain', 'Lens']
	x = ""
	while x == "":
		for token in tokens:
			if token.lower() in homePlayers:
				return 1
				x = 'stop'
			elif token.lower() in awayPlayers:
				return 1
				x = 'stop'
			else:
				continue
		return 0
		x = 'stop'
	


def main(argv):
	print("@RELATION relevance")
	print()
	print("@ATTRIBUTE event NUMERIC")
	print("@ATTRIBUTE player NUMERIC")
	print("@ATTRIBUTE class 	{relevant, irrelevant}")
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
		vector.append(str(eventfeatures(newTokens)))
		vector.append(str(playerfeatures(newTokens)))
		if twanno[:-1] == '0':
			vector.append('irrelevant')
		else:
			vector.append('relevant')
		print(','.join(vector))

		
if __name__ == '__main__':
	main(sys.argv)