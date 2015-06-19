#usr/bin/pyton3.4

import sys

def main(argv):
	tweetfile = open(argv[1], 'r')

	print("@RELATION relevance")
	print("@ATTRIBUTE tweet STRING")
	print("@ATTRIBUTE class 	{1, 0}")
	print("@DATA")

	for line in tweetfile:
		twid, twtime, twtext, twanno = line.split('\t')
		print('"{}",{}'.format(twtext.strip(), twanno[:-1]))


if __name__ == '__main__':
	main(sys.argv)