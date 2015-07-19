#!/usr/bin/python2
# -*- coding: latin-1 -*-
# Medelklass.py - Bot questioning "Medelklass"
#
# Author: Erika "eax" Lygdman - erika@eaxbreakparty.se - @eaxbreakparty
# License: LGPL v3 (or anarchy) kopimi also works - k bai. 
#

import inspect, tweepy, time, re

from apisettings import *
from random import randint
from datetime import datetime

class MedelklassBot:
	twitter = TwitterAPI() # module contains api keys, api settings and main tweet function. twitter.tweet(msg)
	statefile = 'statefile.txt'
	blocklist = 'blocklist.txt'

	
	def debugger(self, text):
		print text, '-', inspect.stack()[1][3], '\b()'

	
	def limit_reached(self):
		self.debugger('API call limit reached... sleeping...')
		time.sleep(90)
		return True
	
	
	def content(self): # <--- Needs more content!
		status = [
			"Hmm... Medelklass? Vad menar du?",
			"Asså definera medelklass...",
			"Finns det en medelklass?",
			"Medelklass är bara ett ord för att splittra arbetarklassen",
			"Vafan menar du med \"Medelklass\"?",
			"Medelklass? Du menar medelinkomsttagare?",
			"Trodde det va arbetarklass mot överklass, var kommer medelklassen in?"
		]
		return status[randint(0,len(status)-1)] 

	##
	## <--- Make blocklist function
	##

	def match_query(self, tweet):
		query = re.compile(r'([Mm]edelklass)\w*')
		match = query.search(tweet)
		if match and 'RT' not in tweet:
			print '\n'
			self.debugger('Query match <3')
			return True	
		else:
			self.debugger('Query didn\'nt match')
			return False


	def get_tweets(self):
		tweetlist = []
		print 'Calling API'
		try:
			# API call to put tweets containing the word 'medelklass'
			for tweet in tweepy.Cursor(self.twitter.api.search,q='medelklass').items(): 
				tweetlist.append(tweet)
		except tweepy.TweepError:
			self.limit_reached()
			pass
		tweetlist.reverse()
		return tweetlist



	def engine(self):
		tweets = self.get_tweets()
		try:
			for tweet in tweets:
				if self.match_query(tweet.text) == True and 'RT' not in tweet.text and tweet.retweeted == False:
					# This is where it'll call the tweet function but currently only
					# prints to command line so it won't spam and can be tested.
					#send = self.content , '@%s' % tweet.user.screen_name
					#twitter.tweet(send)
					#print send
		
					
					print '-' * 25
					print tweet.created_at, tweet.user.screen_name, tweet.id, '\n', tweet.text.encode('utf-8'), '\n'
					print self.content(), '@%s' % tweet.user.screen_name
					print '-' * 25, '\n'
				else:
					self.debugger('Didn\'nt receive a newer list of Tweets meeting conditions, continuing loop...')
					time.sleep(15)
					pass	
		except tweepy.TweepError:
			self.limitReached()
			pass

#	def __init__(self, *args, **kwargs):

def main():
	medelklass = MedelklassBot()
 
	while True:
		medelklass.engine()	

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt: 
		quit()

# TODO
# * Solve sys.excepthook is missind; lost sys.stderr
# * Function to put users in blocklist for two weeks..
# * Something to handle *args **kwargs
# * Function to tweet in a "well manered fashion."
# * Fix if-statement in engine() 
