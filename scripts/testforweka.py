#!usr/bin/python3.4

import sys
import nltk

def playerfeature(tokens):
	relevantWords = ['doelpunt', 'goal', 'rode', 'gele', 'rood', 'geel', 'kaart']
	for token in tokens:
		if token in relevantWords:
			return 1
		else:
			return 0


def main(argv):
	annotatedfile = open(argv[1], 'r')
	print("@RELATION relevance")
	print()
	print("@ATTRIBUTE player NUMBER")
	print("@ATTRIBUTE event NUMBER")
	print("@ATTRIBUTE identifier NUMBER")
	print("@ATTRIBUTE class 	{relevant, irrelevant}")
	for line in annotatedfile:
		twid, twtime, twtext, twanno = line.split('\t')
		tokens = nltk.word_tokenize(twtext)
		print(playerfeature())

if __name__ == '__main__':
	main(sys.argv)