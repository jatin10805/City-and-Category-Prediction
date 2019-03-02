import tweepy
import unicodedata
import collections
import operator
import numpy as np
import pandas as pd


consumer_key =  ''
consumer_secret = ''
access_token =  ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

input_category = pd.read_csv('categories_screen.csv')
category = []
tweet_list=[]
for i in range(len(input_category['Screen_name'])):
    stuff = api.user_timeline(screen_name = input_category['Screen_name'][i], count = 200,include_rts = True)
    for status in stuff:
        string = str(unicodedata.normalize('NFKD' ,status.text).encode('ascii','ignore'))
        print(string)
        tweet_list.append(string)
        category.append(input_category['Category'][i])

train_dict = {'Tweets':tweet_list,'Category':category}
train_dataset = pd.DataFrame(data=train_dict)
print(train_dataset.columns)
train_dataset.to_csv('Final_dataset.csv',index=False)
        
