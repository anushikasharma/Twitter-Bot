import tweepy
import pandas as pd
from IPython.display import display
import re
from textblob import TextBlob
import numpy as np



Consumer_Key="pEaRIdm4rvACGyzGWmaiALy2g"
Consumer_Secret="rgFdSuiJ6VVF3pxpdJVPIX5qb2WamZ4lrs7s0MgMK8YWhak6Yq"
Access_Token="1011804593313837056-qMsdKxKriAqH9f7DtvzItcbKpd1sFb"
Access_Token_Secret="E8KjsEvZBCcD1ixPKxHi7flgESsVnZjDhoYmCWMps6Baj"


auth = tweepy.OAuthHandler( Consumer_Key,Consumer_Secret )
auth.set_access_token( Access_Token,Access_Token_Secret )
api = tweepy.API(auth,wait_on_rate_limit=True)

a=input("enter the item you want to search ")
b=int(input("enter the no of tweets "))
results =[]
for tweet in tweepy.Cursor( api.search,q=a,lang="en").items(b):
    results.append( tweet )



def tweets_df(results):
    id_list = [tweet.id for tweet in results ]
    data_set = pd.DataFrame(id_list,columns=[ "id"] )

    data_set["text"] = [tweet.text for tweet in results]
    data_set["created_at"] = [tweet.created_at for tweet in results]
    data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
    data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
    data_set["user_location"] = [tweet.author.location for tweet in results]
    data_set["Hashtags"] = [tweet.entities.get( 'hashtags' ) for tweet in results]

    return data_set


data_set = tweets_df( results )

print(data_set)


# sentiment analysis

def clean_tweet(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-20]+)|([^0-20A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):

    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

data_set['SA'] = np.array([ analize_sentiment(tweet) for tweet in data_set['text'] ])



display(data_set.head())
pos_tweets = [ tweet for index, tweet in enumerate(data_set['text']) if data_set['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data_set['text']) if data_set['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data_set['text']) if data_set['SA'][index] < 0]
data_set.to_csv( 'example.csv' )



print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data_set['text'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data_set['text'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data_set['text'])))




# count the no of followers
c=input("enter the user")
user=api.get_user(c)
print(user.screen_name)
print(user.followers_count)


# tweet a message
message = "update my twitter account!"
api.update_status(status=message)
print("Tweeted: {}".format(message))




for status in tweepy.Cursor(api.home_timeline).items(10):
    print(status.text)
    
# location ,lang,timezone
def location():
    q=input("enter the user")
    search_results=api.search(q)
    for search_result in search_results:
        print('location=',search_result.user.location)
        print( 'lang=',search_result.user.lang )
        print( 'time_zone',search_result.user.time_zone )
a=location()


# analyze top tweets
from collections import Counter

from nltk.corpus import *
list=[]

stop_words=set(stopwords.words('english'))
    # print(stopwords)
for tweet in tweepy.Cursor( api.search,q="realDonaldTrump",lang="en" ).items(10):
    results.append( tweet )
    print( tweet.created_at,tweet.text )
    text=tweet.text
    list1=text.join(re.findall("[a-z][^A-Z]*",text)).split()
    list1=re.sub("http\S+\s"," ",text).split()
    list1 = re.sub( "RT|cc"," ",text ).split()
    list1 = re.sub( "#\S+"," ",text ).split()
    list1 = re.sub( "@\S+"," ",text).split()
    list1 = re.sub( "[%s]" % re.escape(":!")," ",text).split()
    list1= re.sub( "\s+"," ",text).split()
    # print(list1)
    for word in list1:
        if word not in stop_words:
            list.append(word)
count=Counter(list).most_common(3)
print(count)



#compare the tweets
a=input("first")
b=input("second")
c=input("words used by first user")
d=input("words used by second user")
tweets=api.search(a)
tweets2=api.search(b)
s1=''
s2=''
for tweet in tweets:
    s1+=tweet.text
print(s1.count(c))
for tweet in tweets2:
    s2+=tweet.text
print(s2.count(d))
