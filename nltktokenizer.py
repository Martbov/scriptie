import nltk
import sys
from itertools import chain
import pickle
import random
from collections import Counter
import collections
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import DutchStemmer

#http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
#http://streamhacker.com/2010/05/17/text-classification-sentiment-analysis-precision-recall/

wnl = WordNetLemmatizer()
pnl = DutchStemmer()

def tweetFilter(tokens):
	playerlist = [	'iker', 'casillas',
					'cesar', 'azpilicueta', 'tanco',
					'gerard', 'piqué',
					'jordi', 'alba', 'ramos',
					'sergio', 'ramos', 'garcía',
					'andrés', 'iniesta',
					'david', 'silva',
					'francesc', 'fabregas',
					'sergio', 'busquets',
					'xabier', 'alonso',
					'pedro', 'rodriguez', 'ledesma',
					'xavier', 'hernández', 'creus',
					'diego', 'costa', 
					'fernando', 'jose', 'torres', 'sanz',
					'jasper', 'cillessen',
					'bruno', 'martins', 'indi',
					'daryl', 'janmaat',
					'ron', 'vlaar',
					'stefan', 'de', 'vrij', 'devrij',
					'joël', 'veltman',
					'arjen', 'robben', 'arjenrobben',
					'daley', 'blind',
					'jonathan', 'de', 'guzman',
					'georginio', 'wijnaldum',
					'nigel', 'de', 'jong',
					'wesley', 'sneijder',
					'robin', 'van', 'persie', 'vanpersie'
					'jeremain', 'lens']
	clubList = ['spanje', 'nederland', 'spaned', 'spanjenederland']
	newTokens = []
	for token in tokens:
		if not token.startswith('@'):
			if not token.startswith('http'):
				if not token.startswith('"'):
					if not token == 'RT':
						newTokens.append(pnl.stem(token.lower()))
	for i in range(len(newTokens)):
		for ch in newTokens[i]:
			if ch in ['!', '?', ',', '.', '(', ')', '#', '/', '\\']:
				newTokens[i] = newTokens[i].replace(ch, "")
	#for i, token in enumerate(newTokens):
	#	if token in playerlist:
	#		newTokens[i] = newTokens[i].replace(token, 'PLAYER')
	#	if token in clubList:
	#		newTokens[i] = newTokens[i].replace(token, 'CLUB')
	#print(newTokens)
	return newTokens

def main(argv):
	result = []
	irrelevantTweets = []
	for line in open(argv[1]):
		twid, twtime, twtext, twanno = line.split('\t')
		tokens = twtext.split()
		newTokens = tweetFilter(tokens)
		newText = ' '.join(newTokens)
		if twanno[:-1] == '0':
			irrelevantTweets.append((newText, 'irrelevant'))
		else: # if twanno[:-1] == '1'
			result.append((newText, 'relevant'))

	print(len(result))
	print(len(irrelevantTweets))
	result = list(set(result))
	irrelevantTweets = list(set(irrelevantTweets))
	print(len(result))
	print(len(irrelevantTweets))
	irrelevantTweets = random.sample(irrelevantTweets, len(result))
	result.extend(irrelevantTweets)
	
	random.shuffle(result)
	trainData = result

	stopWordList = []
	for word in open('stopwords.txt', 'r'):
		stopWordList.append(word[:-1])
	vocabulary = list(set(chain(*[nltk.word_tokenize(i[0]) for i in trainData])))
	for word in vocabulary[:]:
		if word in stopWordList or word.isdigit() or len(word) < 2:
			vocabulary.remove(word)
	

	vocC = Counter(vocabulary)
	mostC = set([word for word, n in vocC.most_common(500)])
	print("Length of vocabulary is {}".format(len(vocabulary)))
	     
       

	line = 0
	feature_set = []
	for sentence, tag in trainData:
		features = {}
		
		sentenceTokens = set(nltk.word_tokenize(sentence))
		for word in mostC:				
			
			if word in sentenceTokens:
				features[word] = True
			else:
				features[word] = False	
		
		feature_set.append((features, tag))	
		#print("Regel {} van {}".format(line, len(trainData)))
		line = line +1
	
	
	
	trainSplit = int(0.8 * len(feature_set))
	trainData = feature_set[:trainSplit]
	testData = feature_set[trainSplit:]	

	classifier = nltk.NaiveBayesClassifier.train(trainData)
	#print(nltk.classify.accuracy(classifier,testData))


	testSentence = ' Wat een doelpunt van van persie spaned'
	print(classifier.classify(createFeatures(testSentence, mostC)))
	dist = classifier.prob_classify(createFeatures(testSentence, mostC))
	for label in dist.samples():
   		print("{} - {}".format(label, dist.prob(label)))


	print(classifier.show_most_informative_features(5))

	refsets = collections.defaultdict(set)
	testsets = collections.defaultdict(set)
	ref = []
	tagged = []
	
	for i, (feats, label) in enumerate(testData):
	    refsets[label].add(i)
	    observed = classifier.classify(feats)
	    testsets[observed].add(i)
	    ref.append(label)
	    tagged.append(observed)


	
	print(nltk.metrics.ConfusionMatrix(ref, tagged))
	print ('Relevant precision:', nltk.metrics.precision(refsets['relevant'], testsets['relevant']))
	print ('Relevant recall:', nltk.metrics.recall(refsets['relevant'], testsets['relevant']))
	print ('Relevant F-measure:', nltk.metrics.f_measure(refsets['relevant'], testsets['relevant']))
	print ('Irrelevant precision:', nltk.metrics.precision(refsets['irrelevant'], testsets['irrelevant']))
	print ('Irrelevant recall:', nltk.metrics.recall(refsets['irrelevant'], testsets['irrelevant']))
	print ('Irrelevant F-measure:', nltk.metrics.f_measure(refsets['irrelevant'], testsets['irrelevant']))


def createFeatures(tweet,mostC):
	features ={}
	sentenceTokens = set(nltk.word_tokenize(tweet))
	for word in mostC:				
		
		if word in sentenceTokens:
			features[word] = True
		else:
			features[word] = False	
	return features

if __name__ == '__main__':
	main(sys.argv)