import tweepy
import collections
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import unicodedata
import time
import csv

consumer_key =  ''
consumer_secret = ''
access_token =  ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

city_file = open('indian_cities.enc')
city_list = city_file.read()
city_list = city_list.split('\n')
city_list = city_list[0:(len(city_list)-1)]

ref_dict_dataframe = pd.read_csv('ref_city_dataframe.csv')
ref_city_percentage = {}
for i in range(len(ref_dict_dataframe)):
        ref_city_percentage[ref_dict_dataframe['city_name'][i]] = ref_dict_dataframe['city_percentage'][i]

buckets = pd.read_csv('category_bucket_main.csv')
bucket_cat_dict = {}
bucket_sub_dict = {}
for i in range(len(buckets)):
        bucket_cat_dict[buckets['handle'][i]]= buckets['category'][i]
        bucket_sub_dict[buckets['handle'][i]]= buckets['sub_category'][i]

def city(screen_name):
        ids = []
        for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
            ids.extend(page)

        screen_name_input = []
        location_input = []
        chunk_divider = int(len(ids)/100)
        for j in range(chunk_divider+1):
            if j == chunk_divider:
                try:
                    chunk = ids[j*100:]
                    for i in api.lookup_users(user_ids=chunk):
                        screen_name_input.append(i.screen_name)
                        location_input.append(i.location)
                except:
                    continue
            else:
                chunk = ids[j*100:(j+1)*100]
                for i in api.lookup_users(user_ids=chunk):
                    screen_name_input.append(i.screen_name)
                    location_input.append(i.location)
                #print(count)
        count =0
        location_ascii = []
        for i in location_input:
            location_ascii.append(unicodedata.normalize('NFKD' ,i).encode('ascii','ignore'))
        followers_location = {"screen_name":screen_name_input,"city":location_ascii}
        followers_dataframe = pd.DataFrame(data = followers_location)
        return followers_dataframe

def get_output(user):
        start_time = time.time()
        user_city_list = []
        followers_df = city(user)
        print("time to get followers info : ")
        print("--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        for i in followers_df['city']:
                if(type(i)==float):
                        continue
                else :
                        for j in city_list:
                                if j.lower() in str(i.lower()):
                                        user_city_list.append(j)
        if(len(user_city_list)<1):
                return ''
                    
        counter = collections.Counter(user_city_list)
        counter = dict(counter)
        #counter = sorted(dict(counter).iteritems(),key = lambda (k,v) : (v,k))
        city_names = []
        city_count = []
        for  i in counter.keys():
                city_names.append(i)
                city_count.append(counter[i])
        city_count_sum = sum(city_count)
    
        if city_count_sum == 0:
                city_count_sum = 1
        city_dict = {}
        for i in city_list:
                city_dict[i] = 0
        for i in range(len(counter)):
                city_dict[city_names[i]] = city_count[i]
        user_city_percentage = {}
        for i in city_dict.keys():
                user_city_percentage[i]=(float(city_dict[i])/float(city_count_sum))*100
      #  user_city_dict1 = {"city_name":list(city_dict.keys()),"city_value":list(city_dict.values()),"city_percentage":city_percentage}
      #  user_dict_dataframe1 = pd.DataFrame(data = user_city_dict1)
        max1 = user_city_percentage['Satara']-ref_city_percentage['Satara']
        predicted_city = str('Satara')

        for i in user_city_percentage.keys() :
                if user_city_percentage[i]-ref_city_percentage[i] > max1:
                        max1 = user_city_percentage[i]-ref_city_percentage[i]
                        predicted_city = i

            
        return str(predicted_city)
    


def category_city_list(screen_name):
        start_time = time.time()
        category = ''
        sub_category = ''
        city = ''
        handle = ''
        print(str(screen_name)+" : ")
        ids = []
        
        for page in tweepy.Cursor(api.friends_ids, screen_name=screen_name).pages() :
                ids.extend(page)

        friends_screen_name = []
        chunk_divider = int(len(ids)/100)
        print("Time for getting user ids : ")
        print("--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        for j in range(chunk_divider+1):
                if chunk_divider == 0 :
                        try:
                                chunk = ids
                                for i in api.lookup_users(user_ids=chunk):
                                        friends_screen_name.append(i.screen_name)
                        except:
                                continue
                        
                elif j == chunk_divider:
                        try:
                                chunk = ids[j*100:]
                                for i in api.lookup_users(user_ids=chunk):
                                        friends_screen_name.append(i.screen_name)
                        except:
                                continue
                else:
                        chunk = ids[j*100:(j+1)*100]
                        for i in api.lookup_users(user_ids=chunk):
                                friends_screen_name.append(i.screen_name)
        print("Time for getting user handle : ")
        print("--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        categorical = []
        sub_categorical = []
        for i in friends_screen_name:
                try:
                        categorical.append(str(bucket_cat_dict[i]))
                        sub_categorical.append(str(bucket_sub_dict[i]))
                except:
                        continue
        counter_cat = collections.Counter(categorical)
        counter_sub = collections.Counter(sub_categorical)
        counter_cat_dict = dict(counter_cat)
        counter_sub_dict = dict(counter_sub)
        if(len(counter_cat_dict)>0):
                category = max(counter_cat_dict,key=counter_cat_dict.get)
        if(len(counter_sub_dict)>0):
                sub_category = max(counter_sub_dict,key=counter_sub_dict.get)
	
        print("Time for comparing categories :")
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Time for getting followers data :")
        start_time = time.time()
        city = get_output(screen_name)
        handle = str(screen_name)
        print ("handle = "+handle)
        print ("city = "+str(city))
        print ("category = "+category)
        print ("sub_category = "+sub_category)
        return handle,str(city),category,sub_category
	
"""
    dict_all = {'handle':handle,'category':category,'sub_category':sub_category,'city':city}
    df_all = pd.DataFrame(data=dict_all)
    df_all.to_csv('final_output.csv',index=False)
    print(df_all)
"""

with open(r'final_output.csv','a',newline='') as csvfile:
        field_names = ['Handle','City','Category','Sub_category']
        writer = csv.DictWriter(csvfile,fieldnames=field_names)
        #put the list of users screen_name below in square brackets
        screen_name = []
        for i in screen_name:
                Handle,City,Category,Sub_category=category_city_list(i)
                writer.writerow({'Handle':Handle,'City':City,'Category':Category,'Sub_category':Sub_category})
csvfile.close()


