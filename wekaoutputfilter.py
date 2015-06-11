#usr/bin/python3.4

import sys


def main(argv):
	wekaOutput = open(argv[1], 'r')
	tweetFile = open(argv[2], 'r')
	classifications = []
	for line1, line2 in zip(wekaOutput, tweetFile):
		splitline = line1.split()
		twid, twtime, twtext, twanno = line2.split('\t')
		if len(splitline) == 6:
			if '?' in splitline:
				if '+' in splitline:
					#classifications.append((line2, int(splitline[2][0])-1))
					print(twid + '\t' + twtime + '\t' + twtext + '\t' + str(int(splitline[2][0])-1))
	

if __name__ == '__main__':
	main(sys.argv)