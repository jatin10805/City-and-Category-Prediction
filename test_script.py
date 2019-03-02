from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from time import time
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle 
import pandas as pd
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.ensemble import RandomForestClassifier
import tweepy
import unicodedata
import collections
import operator
from sklearn.neighbors import KNeighborsClassifier
import numpy as np


consumer_key =  ''
consumer_secret = ''
access_token =  ''
access_secret = ''

category_list = pd.read_csv('output_encode.csv')
inverse_category_dict = {}

category_dict = {}
for i in range(len(category_list)):
    category_dict[category_list['Category'][i]]=category_list['Number'][i]
    inverse_category_dict[category_list['Number'][i]]=category_list['Category'][i]

    
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)



complete_data = pd.read_csv('Final_dataset.csv')
#complete_data = shuffle(complete_data)
category_encode = pd.read_csv('output_encode.csv')
labels = []

#appending labels for tweets
for i in range(len(complete_data)):
    for j in range(len(category_encode)):
        if(complete_data['Category'][i]==category_encode['Category'][j]):
            labels.append(category_encode['Number'][j])
complete_data  = complete_data['Tweets']

#splitting dataset 
X_train, X_test, y_train, y_test = train_test_split( complete_data, labels, test_size=0.01, random_state=42)

#converting into float
vectorizer = TfidfVectorizer(sublinear_tf=True,stop_words='english') #apply prepreocessing and stopwords
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

#training different algorithms
clf1 = Perceptron(max_iter= 60)
clf2 = BernoulliNB(alpha=.01)
clf3 = MultinomialNB(alpha=.01)
clf4 = RandomForestClassifier(n_estimators = 30)
clf5 = KNeighborsClassifier(n_neighbors=2)
 
print("n_samples: %d, n_features: %d" % X_train.shape)
 
clf1.fit(X_train, y_train)
clf2.fit(X_train, y_train)
clf3.fit(X_train, y_train)
clf4.fit(X_train, y_train)
clf5.fit(X_train, y_train)

#lists for saving output
final_ans_per = []
final_ans_ber = []
final_ans_mul = []
final_ans_rf = []
final_ans_knn = []
screen_name = []

#final test for categories

def final_category_output(screen_name1):
    tweet_list=[]
    stuff = api.user_timeline(screen_name = screen_name1, count = 200,include_rts = True)
    for status in stuff:
        string = str(unicodedata.normalize('NFKD' ,status.text).encode('ascii','ignore'))
        tweet_list.append(string)
    dictf = {'Tweets':tweet_list}
    df = pd.DataFrame(data = dictf)
    X_test = df['Tweets']
    labels = []
    for i in df:
        labels.append(0) 
    X_test = vectorizer.transform(X_test)
    #predicing category
    final_list1 = clf1.predict(X_test)
    final_list2 = clf2.predict(X_test)
    final_list3 = clf3.predict(X_test)
    final_list4 = clf4.predict(X_test)
    final_list5 = clf5.predict(X_test)
    final_output_dict1=dict(collections.Counter(final_list1))
    final_output_dict2=dict(collections.Counter(final_list2))
    final_output_dict3=dict(collections.Counter(final_list3))
    final_output_dict4=dict(collections.Counter(final_list4))
    final_output_dict5=dict(collections.Counter(final_list5))
    v1=list(final_output_dict1.values())
    k1=list(final_output_dict1.keys())
    final_output_1 = k1[np.argmax(v1)]
    v2=list(final_output_dict2.values())
    k2=list(final_output_dict2.keys())
    final_output_2 = k2[np.argmax(v2)]
    v3=list(final_output_dict3.values())
    k3=list(final_output_dict3.keys())
    final_output_3 = k3[np.argmax(v3)]
    v4=list(final_output_dict4.values())
    k4=list(final_output_dict4.keys())
    final_output_4 = k4[np.argmax(v4)]
    v5=list(final_output_dict5.values())
    k5=list(final_output_dict5.keys())
    final_output_5 = k5[np.argmax(v5)]
    final_ans_per.append(final_output_1)
    final_ans_ber.append(final_output_2)
    final_ans_mul.append(final_output_3)
    final_ans_rf.append(final_output_4)
    final_ans_knn.append(final_output_5)
    screen_name.append(screen_name1)
    print(inverse_category_dict[final_output_1])
    print(inverse_category_dict[final_output_2])
    print(inverse_category_dict[final_output_3])
    print(inverse_category_dict[final_output_4])
    print(inverse_category_dict[final_output_5])

test_category = pd.read_csv('test.csv')

for i in test_category['Screen_name']:
    final_category_output(i)

#accuracy score
actual_score = list(test_category['Score'])
score1 = metrics.accuracy_score(actual_score,final_ans_per)
score2 = metrics.accuracy_score(actual_score, final_ans_ber)
score3 = metrics.accuracy_score(actual_score, final_ans_mul)
score4 = metrics.accuracy_score(actual_score, final_ans_rf)
score5 = metrics.accuracy_score(actual_score, final_ans_knn)

print("perceptron:   %0.3f" % score1)
print("BernoulliNB:   %0.3f" % score2)
print("MultinomialNB:   %0.3f" % score3)
print("RandomForest:   %0.3f" % score4)
print("NearestNieghbor   %0.3f" % score5)

#saving into file final.csv

final_output = {'screen_name':screen_name,'perceptron':final_ans_ber,'BernoulliNB':final_ans_per,'MultinomialNB':final_ans_mul,'RandomForest':final_ans_rf,'KNN':final_ans_knn}
final_df  = pd.DataFrame(data=final_output)
final_df.to_csv('final.csv',index=False)
