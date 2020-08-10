#==========================
#Import necessary libraries
#==========================

import tweepy
import re
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#==========================
#Method to clean the Tweets
#==========================

def cleanTweet(tw):
 #Convert to lowercase
 tw=tw.lower() 

 #Remove unwnted text, user handles (@), hashtags(#), http/s, www
 tw=re.sub('http\S+|www\S+|https\S+', ' ', tw)
 tw=re.sub('(@[a-zA-Z0-9]+)',' ',tw)
 tw=re.sub('(#[a-zA-Z0-9]+)',' ',tw)
 tw=re.sub('[^a-zA-Z0-9]',' ',tw)
 
 tw=tw.split() 
 
 #Remove English stopwords
 words=[ w for w in tw if not w in set(stopwords.words("english"))]
 
 print("\n")
 #Lemmatizing
 lemmatizer = WordNetLemmatizer()
 words_final = [lemmatizer.lemmatize(w, pos='a') for w in words]
  
 words_final=' '.join(words_final)
 
 print("\n") 
 return words_final

#====================================
#Method to get Sentiment for the tweet
#====================================

def get_sentiment(tw): 
 tw_blb=TextBlob(tw) 
 senti=tw_blb.sentiment.polarity
 if senti>0:
  senti_text="Positive"
 elif senti<0: 
  senti_text="Negative"
 else:
  senti_text="Neutral"
  
 return senti_text


#========================================
#Use Tweepy API to connect to Twitter...
#Register an App and get the below keys
#========================================

consumer_key="XXXXXXXXXXXX"
consumer_key_secret="XXXXXXXXXXXX"
accesstoken_key="XXXXXXXXXXXX"
accesstoken_secret="XXXXXXXXXXXX"

auth=tweepy.OAuthHandler(consumer_key,consumer_key_secret)
auth.set_access_token(accesstoken_key,accesstoken_secret)

api=tweepy.API(auth)

#==========
#Get Tweets
#==========

#tweets=api.search(q="@BBCWorld",count=20)
tweets=api.user_timeline(screen_name="@BBCWorld",count=20)

#======================
#Pre-process the tweets
#======================

final_list=[]
for t in tweets:
 clean_tweets={} 
 twt=cleanTweet(t.text.encode("utf-8"))
 clean_tweets["rawTweet"]=t.text.encode("utf-8")
 clean_tweets["cleanedTweet"]=twt
 clean_tweets["sentiment"]=get_sentiment(twt)
 final_list.append(clean_tweets)

#========================================
#Print each resultant tweet and sentiment
#========================================

"""
for tweet_senti in  final_list:
 print(tweet_senti["rawTweet"])
 print(tweet_senti["cleanedTweet"])
 print(tweet_senti["sentiment"])
 print("\n")
"""
 
#==========================================
#==============POSITIVE TWEETS=============
#==========================================

#Positive tweets (%)
ptweets=[]
for t in final_list: 
 if t["sentiment"] == "Positive":
  ptweets.append(t)

pos_per=100*len(ptweets)/len(final_list)
print("Positive tweets (%): "+str(pos_per))

#First 3 tweets
print("First three Positive tweets:")
for p in ptweets[:3]:
 print(p)
 print("\n")

#==========================================
#==============NEGATIVE TWEETS=============
#==========================================

ntweets=[]
#Negative tweets(%)
ntweets=[t for t in final_list if t["sentiment"]=="Negative" ]
neg_per=100*len(ntweets)/len(final_list)
print("Negative tweets (%): "+str(neg_per))

#First 3 tweets
print("First three Negative tweets:")
for n in ntweets[:3]:
 print(n)
 print("\n")

#==========================================
#==============NEUTRAL TWEETS==============
#==========================================

#Neutral tweets (%)
neutweets=[]
neutweets=[t for t in final_list if t["sentiment"]=="Neutral" ]
neu_per=(100*(len(final_list)-(len(ptweets)+len(ntweets))))/len(final_list)
print("Neutral tweets (%): "+str(neu_per))

#First 3 tweets
print("First three Neutral tweets:")
for nl in neutweets[:3]:
 print(nl)
 print("\n")

