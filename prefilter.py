#!usr/bin/python3.4

import sys

def main(argv):
	tweetfile = argv[1]
	rawTweetData = open(tweetfile, encoding='utf-8')
	for line in rawTweetData:
		tweetID, tweetDate, tweetUser, tweetText = line.split('\t')
		tweetUser = str(tweetUser)
		tweetText = str(tweetText)
		invalidUsers = ['sport1nl', 'nosvoetbal', 'voetbalpings', 'voetbalzonenl', 'voetbalprimeur', 'by433', '433live', '443nl' 'foxsportslive', 'nu_sportslive', 'livesports_hd', 'livefootball']
		if tweetUser.lower() not in invalidUsers:
			conditions = ['chili', 'nederland', '#nedchi']
			eventTypes = ['doelpunt', 'goal', 'rode', 'gele', 'rood', 'geel', 'kaart']
			if any(condition in line for condition in conditions) and any(eventtype in line for eventtype in eventTypes):
				print(tweetID + "\t" + tweetDate[11:19] + "\t" + tweetText[:-1] + "\t" + "0", file=sys.stdout)
				print("{}\t{}\t{:>140}\t?".format(tweetID, tweetDate[11:19], tweetText[:-1]))
				#for word in tweetText.split():
				#	print(word, file=sys.stdout)
				#print()
	

if __name__ == '__main__':
	main(sys.argv)