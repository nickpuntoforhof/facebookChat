# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 10:58:07 2018

@author: Noah
"""

#Load Packages and Print Working Directory

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import bs4
import re
from collections import Counter
import collections
from operator import itemgetter
from datetime import datetime
import matplotlib.pyplot as plt


#set working directory
from os import chdir, getcwd
chdir('c:/Users/Noah/Documents/facebook_analysis')
wd=getcwd()
print(wd)


## Import html ##
url = 'C:/Users/Noah/Downloads/facebook-ns/messages/inbox/memeLovers_ySI8aJ3XXA/message.html'
#C:\Users\Noah\Downloads\facebook-ns\messages\inbox\memeLovers_ySI8aJ3XXA

with open(url, "r", encoding="utf-8") as meme_lovers:
        soup = bs4.BeautifulSoup(meme_lovers.read(), "lxml")



##############################################################################
# find post frequency of all users
users = soup.find_all("div",class_= "_3-96 _2pio _2lek _2lel")

print(users)
type(users)
#remove html tags from users

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('',text)

clean_users = []
for i in range(len(users)):
    clean_users.append(remove_tags(users[i].text))
    
#create histogram of post frequency
post_counts = Counter(clean_users)
user_df = pd.DataFrame.from_dict(post_counts, orient='index')
user_hist = user_df.plot(kind = 'bar', 
             title = "Amount of posts by user in meme Lovers from March 5, 2018 to December 25, 2018",
             legend = False,
             sort_columns = True,
             color = "purple",
             figsize = (10,7))

#now find all react posts
reacts = soup.find_all("li")
print(reacts)

def clean_text(text):
    temp_text = re.compile('<.*?>').sub('', text) #removes all text in html tags
    temp_text = temp_text.replace("\n"," ") #rep newline with space
    temp_text = temp_text.replace("\u200d♂"," ") #remvoes unicode escapes
    temp_text = re.sub(r'^https?:\/\/.*[\r\n]*', '',
                              temp_text,
                              flags=re.MULTILINE) #deletes urls
    return temp_text

clean_reacts = []
#run clean_text on each element of reacts list
for i in range(len(reacts)):
    clean_reacts.append(clean_text(reacts[i].text))
    
    
react_counts = Counter(clean_reacts)

print("Most reacts by User-React Pair")
for k in range(len(react_counts.most_common())):
    if k < 30:
        print(react_counts.most_common()[k])

#now find all text posts
textp = soup.find_all("p")

print(textp)
type(textp)

#clean the list of text by writing a function that will do a
#numerous things to the text as denoted below.



clean_textp = []

#run clean_text on each element of textp list
for i in range(len(textp)):
    clean_textp.append(clean_text(textp[i].text))


#remove empty strings from list
red_textp = list(filter(None, clean_textp))
    
len(clean_textp)
len(red_textp)

# concatenate list of strings into one string, with each element of
# the list separated by spaces

meme_lovers_dirty = ' '.join(red_textp)

meme_lovers_text = re.sub(r'([^\s\w]|_)+', '', meme_lovers_dirty)


# so now we have meme_lovers_text, a single string of
# only alphanumeric characters separated by spaces

# let's count the frequency which words appear
# create an empty dictionary called word count, add
# any new word to word count, add 1 to count if word has been
# encountered before
wordcount = {}

for word in meme_lovers_text.lower().split():
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1
        

wordcount_filter = {k: v for k, v in wordcount.items() if v >= 10}

wordcount_sort = collections.OrderedDict(sorted(wordcount_filter.items(), 
                               key = itemgetter(1), 
                               reverse = True))

print(wordcount_sort)




#### now I'm gonna create a dataframe with each post's date and 
#### the name of each poster.  Ultimately, i'm looking to create a cumulative
#### graph of each poster's post total by date.
usernames_html = soup.find_all("div",class_="_3-96 _2pio _2lek _2lel")
dates_html = soup.find_all("div", class_="_3-94 _2lem")

#extract just the text from these beautiful soup objects.put text into 2 lists

post_date_str = [] 
post_user_name = []

for i in range(len(usernames_html)):
        post_user_name.append(usernames_html[i].text)


for i in range(len(dates_html)):
        post_date_str.append(dates_html[i].text)

# put these two lists into pandas dataframe
posts_dataframe = pd.DataFrame(
        {'userName' : post_user_name,
         'postDateTimeStr' : post_date_str[1:]
         })
    
# use pd.to_datetime to convert date strings into date object

posts_dataframe['postDate'] = pd.to_datetime(posts_dataframe['postDateTimeStr'])

posts_dataframe['justDate'] = posts_dataframe['postDate'].dt.date

# ok! now we got a dataframe of exactly what we need to get this graph.
# now we need to manipulate this data into exactly what we need.
# we need the columns to be each user, the first column to be the datetime
# of each post, and the values of each user column to be the amount of 
# posts they have made up to that date.

#sorty by date
pdat = posts_dataframe.sort_values(by="justDate", ascending=True) 

uniqueUsers = pdat['userName'].unique()

#groupby date and username and count the size of each group
gdat = pdat.groupby(['justDate','userName']).size()
gdat = gdat.reset_index() #split index into date and name columns

#rename columns
gdat.columns = ['date','userName','count']

#reshape data to wide format
widedat = pd.pivot_table(gdat, values='count',index=["date"],columns='userName')

#replace nans in data with 0's
widedat = widedat.fillna(0)

#create cumulative data

cumdat = widedat.cumsum().reset_index()

#wide to tall data

finaldat = pd.melt(cumdat, id_vars = 'date', value_vars = uniqueUsers)

finaldat.to_csv("goonsquadfinal.csv")



             
    
    



