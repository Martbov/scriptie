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

def document_features(document, word_features):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains({})'.format(word)] = (word in document_words)
	return features

def main(argv):
	annotatedfile = open(argv[1], 'r')
	allwords = []
	twtextList = []
	for line in annotatedfile:
		twid, twtime, twtext, twanno = line.split('\t')
		tokens = twtext.split()
		newTokens = tweetFilter(tokens)
		twtextList.append([newTokens, twanno[-1]])
		for token in newTokens:
			allwords.append(token)
	for doc, anno in twtextList:
		print(doc, anno)
	all_words = nltk.FreqDist(allwords)
	word_features = list(all_words)[:1000]
	featuresets = [(document_features(document, word_features), anno) for (document, anno) in twtextList]
	train_set, test_set = featuresets[100:], featuresets[:100]
	classifier = nltk.NaiveBayesClassifier.train(train_set)
	print(nltk.classify.accuracy(classifier, test_set))
	print(classifier.show_most_informative_features(5))
	


		
if __name__ == '__main__':
	main(sys.argv)