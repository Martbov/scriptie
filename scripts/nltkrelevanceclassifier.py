import nltk
import sys
from itertools import chain
import pickle
import random
from collections import Counter
import collections
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import DutchStemmer
from nltk import stem
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


#http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
#http://streamhacker.com/2010/05/17/text-classification-sentiment-analysis-precision-recall/

wnl = WordNetLemmatizer()
pnl = DutchStemmer()

def prefilter(infile):
	rawTweetData = open(infile, encoding='utf-8')
	temp = open('temp', 'w')
	for line in rawTweetData:
		tweetID, tweetDate, tweetUser, tweetText = line.split('\t')
		tweetUser = str(tweetUser)
		tweetText = str(tweetText)
		invalidUsers = ['sport1nl', 'nosvoetbal', 'voetbalpings', 'voetbalzonenl', 'voetbalprimeur', 'by433', '433live', '443nl' 'foxsportslive', 'nu_sportslive', 'livesports_hd', 'livefootball']
		if tweetUser.lower() not in invalidUsers:
			conditions = ['australie', 'australië', 'nederland', '#ausned']
			eventTypes = ['doelpunt', 'goal', 'rode', 'gele', 'rood', 'geel', 'kaart']
			if any(condition in line for condition in conditions) and any(eventtype in line for eventtype in eventTypes):
				#print(tweetID + "\t" + tweetDate[11:19] + "\t" + tweetText[:-1] + "\t" + "0", file=sys.stdout)
				print("{}\t{}\t{:>140}\tanno".format(tweetID, tweetDate[11:19], tweetText[:-1]), file=temp)
				#for word in tweetText.split():
				#	print(word, file=sys.stdout)
				#print()
	
	temp.close()

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
	#clubList = ['spanje', 'nederland', 'spaned', 'spanjenederland']
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
	for i, token in enumerate(newTokens):
		if token in playerlist:
			newTokens[i] = newTokens[i].replace(token, 'PLAYER')
	#	if token in clubList:
	#		newTokens[i] = newTokens[i].replace(token, 'CLUB')
	#print(newTokens)
	return newTokens

def createFeatures(tweet,mostC):
	features ={}
	sentenceTokens = set(nltk.word_tokenize(tweet))
	for word in mostC:						
		if word in sentenceTokens:
			features[word] = True
		else:
			features[word] = False	
	return features

def trainer():
	result = []
	irrelevantTweets = []
	for line in open('gameonlyspanedannotated.txt'):
		twid, twtime, twtext, twanno = line.split('\t')
		"""
		if twanno[:-1] == '0':
			result.append((twtext, 'irrelevant'))
		else:
			result.append((twtext, 'relevant'))
		"""
		tokens = twtext.split()
		newTokens = tweetFilter(tokens)
		newText = ' '.join(newTokens)
		if twanno[:-1] == '0':
			irrelevantTweets.append((newText, 'irrelevant'))
		else: # if twanno[:-1] == '1'
			result.append((newText, 'relevant'))

	result = list(set(result))
	irrelevantTweets = list(set(irrelevantTweets))
	
	#irrelevantTweets = random.sample(irrelevantTweets, len(result))
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
	#print("Length of vocabulary is {}".format(len(vocabulary)))
		 
	   

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
	print(feature_set)
	
	
	trainSplit = int(0.8 * len(feature_set))
	trainData = feature_set[:trainSplit]
	testData = feature_set[trainSplit:]	

	pipeline = Pipeline([('tfidf', TfidfTransformer()), ('chi2', SelectKBest(chi2, k='all')), ('nb', MultinomialNB())])
	classif = SklearnClassifier(pipeline)
	classif.train(trainData)

	#classifier = MultinomialNB.train(trainData)
	classifier = nltk.NaiveBayesClassifier.train(trainData)

	return mostC, trainData, testData, classifier, classif

def main(argv):
	
	mostC, trainData, testData, classifier, classif = trainer()
	"""
	rawTweets = argv[1]
	prefilter(rawTweets)

	newData = open('temp')
	
	minuteList = []
	for line in newData:
		twid, twtime, twtext, twanno = line.split('\t')
		twMinute = str(twtime[:5])
		minuteList.append(twMinute)
		tokens = twtext.split()
		newTweet = ' '.join(tweetFilter(tokens))
		classification = classifier.classify(createFeatures(newTweet, mostC))
		#print(newTweet, classification)

	minuteCounter = Counter(minuteList)
	print(minuteCounter.most_common(10))"""
	
	testSentence = 'wat een geweldige goal door robben #spaned'
	print("Classified as:", classifier.classify(createFeatures(testSentence, mostC)))
	#print("Multinomial classified it as:", classif.classify_many(testSentence))
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
	print('Relevant precision:', nltk.metrics.precision(refsets['relevant'], testsets['relevant']))
	print('Relevant recall:', nltk.metrics.recall(refsets['relevant'], testsets['relevant']))
	print('Relevant F-measure:', nltk.metrics.f_measure(refsets['relevant'], testsets['relevant']))
	print('Irrelevant precision:', nltk.metrics.precision(refsets['irrelevant'], testsets['irrelevant']))
	print('Irrelevant recall:', nltk.metrics.recall(refsets['irrelevant'], testsets['irrelevant']))
	print('Irrelevant F-measure:', nltk.metrics.f_measure(refsets['irrelevant'], testsets['irrelevant']))
	print("Accuracy classifier:", nltk.classify.accuracy(classifier, testData))


if __name__ == '__main__':
	main(sys.argv)