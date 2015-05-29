import sys
from collections import Counter

def main(argv):
	infile = open(argv[1], 'r')
	c = Counter()
	for line in infile:
		tweetID, tweetTime, tweetText, tweetAnnotation = line.split('\t')
		c.update(tweetAnnotation[:-1])

	print(c)

if __name__ == '__main__':
	main(sys.argv)