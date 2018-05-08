# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 19:38:17 2018

@author: Praful
"""
import tweepy
from textblob import TextBlob
import re
import pandas as pd
import nltk
import csv

#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def analysis_plot(var):
    consumer_key = 'FZ2CWGMLhRN9dc1NCLvD4Whux'
    consumer_secret = '068Q0CYmNtbtaivPSntWCt40QC5Yu5Ku5AOiw0hB1LJFvay89p'

    access_token = '960867938864586753-GDERwMnBFrAeEO1LDGHynH02Fq6JjLa'
    access_token_secret = '979YFk00sn1uOj6PbDQi5fKt4RyB45KpQgWzhCAXoZjUi'


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    name = var
    api = tweepy.API(auth)
    dict1 = {}
    #l = tweepy.StdOutListener()
    #stream = tweepy.Stream(auth,l)
    public_tweets = api.search(q=var ,lang="en",count=100)
    print("Running")


    with open("C:\\Users\\Praful\\Desktop\\tweets.csv", "w", encoding='utf-8') as f:
        fieldnames=['tweet','sentiment','stats']
        writer = csv.DictWriter(f, dialect='excel',fieldnames = fieldnames)#, encoding='utf-8')

        writer.writeheader()
        posi = 0
        nega = 0
        neu = 0
        for tweet in public_tweets:

            analysis = TextBlob(tweet.text)
            #print(tweet.text)
            charge = ''
            #analysis = TextBlob(clean_tweet(tweet.text))
            if analysis.sentiment.polarity > 0:
                charge = 'positive'
                posi +=1
            elif analysis.sentiment.polarity == 0:
                charge =  'neutral'
                neu +=1
            else:
                charge =  'negative'
                nega +=1

        #c+=1
            dict1 = { 'tweet':tweet.text,
                     'sentiment':analysis.sentiment,
                     'stats':charge}
            writer.writerow(dict1)
            # set sentiment
        sizes = [nega, posi, neu]
        return sizes




def analysis_plot_fixed_data(var):

    neu = 0
    neg = 0
    posi = 0
    dataset = pd.read_csv("C:\\Users\\Praful\\Desktop\\Dataset\\Tweets.csv")
    x = dataset.iloc[:,1].values
    for i in range (0,100):
        if x[i] == 'neutral':
            neu+=1
        elif x[i] == 'negative':
            neg+=1
        elif x[i] == 'positive':
            posi+=1
    sizes = [neg, posi, neu]
    return sizes
