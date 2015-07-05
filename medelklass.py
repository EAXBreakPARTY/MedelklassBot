#!/usr/bin/python2
# -*- coding: iso-8859-15 -*-
# Medelklass.py - Bot questioning "Medelklass"
#
# Author: Erika "EAX" Lygdman - erika@eaxbreakparty.se - @eaxbreakparty
# License: LGPL v3 (or anarchy)
#

import tweepy, time

from apisettings import *
from random import randint


class MedelklassBot:
	twitter = TwitterAPI() # module contains api keys, api settings and main tweet function. twitter.tweet(msg)
	statefile = 'statefile.txt'

	def debugger(self, text):
		print text
	
	def content(self): # Needs more content!
		status = [
			"Hmm... Medelklass? Vad menar du?",
			"Asså definera medelklass...",
			"Finns det en medelklass?",
			"Medelklass är bara ett ord för att splittra arbetarklassen",
			"Vafan menar du med \"Medelklass\"?",
			"Medelklass? Du menar medelinkomsttagare?"
		]
		return status[randint(0,len(status)-1)] 
	
	def getPrevID(self):
		try:
			f = open(self.statefile, 'r')
			id = int(f.readline())
			f.close()
			return id
		except IOError:
			self.debugger('getPrevID Got IOError, Passing...')
			pass

	def saveID(self, state):
		prevID = self.getPrevID()
		try:
			if state > prevID:
				f = open(self.statefile, 'w')
				f.write(str(state))
				f.close()		
			else:
				self.debugger('New ID smaller than previous stored ID, passing...')
		except IOError:
			self.debugger('saveID got IOError, Passing...')
			pass

	def limitReached(self):
		self.debugger('API call limit reached... sleeping...')
		time.sleep(60 * 15)
		return True

	def getTweets(self):
		sinceID = self.getPrevID()
		tweetList = []
		try:
			# API call to put tweets containing the word 'medelklass' and with greater value than last seen ID.
			for tweet in tweepy.Cursor(self.twitter.api.search,q='medelklass', since_id=sinceID).items(): 
				tweetList.append(tweet)
				
		except tweepy.TweepError:
			if self.limitReached() == True:
				print "getTweets got error"
				pass
		# Returns tweetList in reverse, tweet.id low to high
		# Tweepy Cursor().items() is stupid and fetches tweets high to low.
		tweetList.reverse()
		return tweetList

	def engine(self):
		prevID = self.getPrevID()
		tweets = self.getTweets()
		idList = [] # <--- Problem with appending on increase
		try:
			for tweet in tweets:
				#STÄDA UPP DEN HÄR IF-SATSEN DIN JÄVEL
				if tweet.retweeted == False and 'RT' not in tweet.text and 'medelklass' in tweet.text and tweet.id > prevID:
					print tweet.created_at, tweet.user.screen_name, tweet.id , '\n', tweet.text, '\n'
					print self.content(), ' @%s\n' % tweet.user.screen_name
					idList.append(tweet.id) # <--- Problem with appending on increase after first loop
				else:
					self.debugger('Didn\'nt receive a list of Tweets, continuing loop...')
					continue
		except tweepy.TweepError:
			self.limitReached()
			pass
		if len(idList)-1 > 0: # <--- problem with this if-statement?
			self.saveID(idList[len(idList)-1])
		else:
			self.debugger('idList is empty, continuing loop...') # <--- Most common message after first loop
			pass

def main():
	medelklass = MedelklassBot()
    
	while True:
		medelklass.engine()	

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt: 
		quit()
