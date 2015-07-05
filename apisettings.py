#!/usr/bin/python2
# -*- coding: utf-8 -*-
# api.py - API settings for medelklass bot questioning "Medelklass"
#
# Author: Erika "EAX" Lygdman - erika@eaxbreakparty.se - @eaxbreakparty
# License: LGPL v3

import tweepy

class TwitterAPI:
    def __init__(self):
        consumer_key = "NBjS9SpePCf3Q5YBhBgIuyV01"
        consumer_secret = "s8QPpcAkdcwTRLk4FeagyY405sxiBBZ3s7rz0Z3RuvVa2dOpvh"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = "3318897874-A6i74J0TjUZaGmppM94fZMPH2AKJcoaztTKSE6S"
        access_token_secret = "Wysoa3kn4RunQ2vMEbGY5XThSGy4ivtoBb8IPdcjygCrh"
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
 
    def tweet(self, message):
        self.api.update_status(status=message)
