import tweepy
import pandas as pd
from IPython.display import display
import re
from textblob import TextBlob
import numpy as np
from collections import Counter
from nltk.corpus import *
from tkinter import*
from PIL import Image, ImageTk




auth = tweepy.OAuthHandler( Consumer_Key,Consumer_Secret )
auth.set_access_token( Access_Token,Access_Token_Secret )
api = tweepy.API(auth,wait_on_rate_limit=True)


def show1():
    def getE1():
        return E1.get()

    def getE2():
        return E2.get()


    def getdata():
        getE1()
        a =getE1()

        getE2()
        numberOfTweets = getE2()
        numberOfTweets = int( numberOfTweets )



        results =[]
        for tweet in tweepy.Cursor( api.search,q=a,lang="en").items(numberOfTweets):
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

    r = Tk()
    r.resizable( False,False )
    r.geometry( "300x300" )
    m2 = Frame( r,width=300,height=300,bg="white" )
    m2.pack( fill=BOTH,expand=1 )

    label1 = Label( m2,text="Enter the text you want to search",width=25,height=2,font=('times',15,'italic'),
                    bg="white" )
    label1.grid( row=0,column=0,padx=0,pady=1 )
    E1 = Entry( m2,border=4 )
    E1.grid()
    label2 = Label( m2,text="Enter the no of tweets",width=25,height=2,font=('times',15,'italic'),bg="white" )
    label2.grid( row=2,column=0,padx=1,pady=1 )
    E2 = Entry( m2,border=4 )
    E2.grid()

    butt1 = Button( m2,bg='white',text="Submit",width=20,height=1,borderwidth=3,highlightbackground="black",
                    relief=SOLID,command=getdata )
    butt1.grid( row=4,column=0,pady=15,padx=1 )
    r.mainloop()



# sentiment analysis
def show2():
    def getE1():
        return E1.get()

    def getE2():
        return E2.get()

    def getE3():
        return E3.get()

    def getdata1():
        getE1()
        a = getE1()

        getE2()
        numberOfTweets = getE2()
        numberOfTweets = int( numberOfTweets )

        getE3()
        num = getE3()
        num = int( num )

        results = [ ]
        for tweet in tweepy.Cursor( api.search,q=a,lang="en" ).items( numberOfTweets ):
            results.append( tweet )

        def tweets_df(results):
            id_list = [ tweet.id for tweet in results ]
            data_set = pd.DataFrame( id_list,columns=[ "id" ] )

            data_set[ "text" ] = [ tweet.text for tweet in results ]
            data_set[ "created_at" ] = [ tweet.created_at for tweet in results ]
            data_set[ "retweet_count" ] = [ tweet.retweet_count for tweet in results ]
            data_set[ "user_screen_name" ] = [ tweet.author.screen_name for tweet in results ]
            data_set[ "user_followers_count" ] = [ tweet.author.followers_count for tweet in results ]
            data_set[ "user_location" ] = [ tweet.author.location for tweet in results ]
            data_set[ "Hashtags" ] = [ tweet.entities.get( 'hashtags' ) for tweet in results ]

            return data_set

        data_set = tweets_df( results )

        def clean_tweet(tweet):

            return ' '.join( re.sub( "(@[A-Za-z0-20]+)|([^0-20A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet ).split() )

        def analize_sentiment(tweet):

            analysis = TextBlob( clean_tweet( tweet ) )
            if analysis.sentiment.polarity > 0:
                return 1
            elif analysis.sentiment.polarity == 0:
                return 0
            else:
                return -1

        data_set[ 'SA' ] = np.array( [ analize_sentiment( tweet ) for tweet in data_set[ 'text' ] ] )

        display(data_set.head(num))
        pos_tweets = [ tweet for index,tweet in enumerate( data_set[ 'text' ] ) if data_set[ 'SA' ][ index ] > 0 ]
        neu_tweets = [ tweet for index,tweet in enumerate( data_set[ 'text' ] ) if data_set[ 'SA' ][ index ] == 0 ]
        neg_tweets = [ tweet for index,tweet in enumerate( data_set[ 'text' ] ) if data_set[ 'SA' ][ index ] < 0 ]
        data_set.to_csv( 'example.csv' )

        print( "Percentage of positive tweets: {}%".format( len( pos_tweets ) * 100 / len( data_set[ 'text'])))
        print( "Percentage of neutral tweets: {}%".format( len( neu_tweets ) * 100 / len( data_set[ 'text'])))
        print( "Percentage de negative tweets: {}%".format( len( neg_tweets ) * 100 / len( data_set[ 'text'])))


    r = Tk()
    r.resizable( False,False )
    r.geometry( "300x300" )
    m2 = Frame( r,width=300,height=300,bg="white" )
    m2.pack( fill=BOTH,expand=1 )

    label1 = Label( m2,text="Enter the text you want to search",width=25,height=2,font=('times',10,'italic'),
                    bg="white" )
    label1.grid( row=0,column=0,padx=50,pady=1 )
    E1 = Entry( m2,border=4 )
    E1.grid()
    label1 = Label( m2,text="Enter the no of tweets",width=25,height=2,font=('times',10,'italic'),bg="white" )
    label1.grid( row=2,column=0,padx=1,pady=1 )
    E2 = Entry( m2,border=4 )
    E2.grid()
    label2 = Label( m2,text="Enter the no of tweets you want to analyse",width=45,height=2,font=('times',10,'italic'),
                    bg="white" )
    label2.grid( row=4,column=0,padx=1,pady=1 )
    E3 = Entry( m2,border=4 )
    E3.grid()
    butt1 = Button( m2,bg='white',text="Submit",width=20,height=1,borderwidth=3,highlightbackground="black",
                    relief=SOLID,command=getdata1 )
    butt1.grid( row=6,column=0,pady=15,padx=1 )
    r.mainloop()



#

# count the no of follower

def show3():
    def getE1():
        return E1.get()

    def getdata2():
        getE1()
        user= getE1()


        user=api.get_user(user)
        print(user.screen_name)
        print(user.followers_count)


    r = Tk()
    r.resizable( False,False )
    r.geometry( "300x300" )
    m2 = Frame( r,width=300,height=300,bg="white" )
    m2.pack( fill=BOTH,expand=1 )

    label1 = Label( m2,text="Enter the user name",width=17,height=2,font=('times',25,'italic'),
                    bg="white" )
    label1.grid( row=0,column=0,padx=1,pady=40 )
    E1 = Entry( m2,border=4 )
    E1.grid()
    butt1 = Button( m2,bg='white',text="submit",width=20,height=1,borderwidth=3,highlightbackground="black",
                    relief=SOLID,command=getdata2 )
    butt1.grid( row=4,column=0,pady=15,padx=1 )
    r.mainloop()
#
#


# tweet a message

def show4():
    def getE1():
        return E1.get()

    def getdata3():
        getE1()
        mess = getE1()
        message =mess
        api.update_status(status=message)
        print("Tweeted: {}".format(message))

    r = Tk()
    r.resizable( False,False )
    r.geometry( "300x300" )
    m2 = Frame( r,width=300,height=300,bg="white" )
    m2.pack( fill=BOTH,expand=1 )

    label1 = Label( m2,text="Enter the message you want to tweet",width=32,height=2,font=('times',12,'italic'),
                    bg="white" )
    label1.grid( row=0,column=0,padx=1,pady=40)
    E1 = Entry( m2,border=4 )
    E1.grid()
    butt1 = Button( m2,bg='white',text="Submit",width=20,height=1,borderwidth=3,highlightbackground="black",
                    relief=SOLID,command=getdata3 )
    butt1.grid( row=4,column=0,pady=15,padx=1 )
    r.mainloop()



def show5():
    def getE1():
        return E1.get()

    def getdata4():
        getE1()
        search1 = getE1()



        def location():

            search_results=api.search(search1)
            for search_result in search_results:
                print('location=',search_result.user.location)
                print( 'lang=',search_result.user.lang )
                print( 'time_zone=',search_result.user.time_zone )
        a=location()

    r = Tk()
    r.resizable( False,False )
    r.geometry( "300x300" )
    m2 = Frame( r,width=300,height=300,bg="white" )
    m2.pack( fill=BOTH,expand=1 )

    label1 = Label( m2,text="Enter the item  you want to search",width=25,height=2,font=('times',15,'italic'),
                    bg="white" )
    label1.grid( row=0,column=0,padx=0,pady=40 )
    E1 = Entry( m2,border=4 )
    E1.grid(row=1,column=0)
    butt1 = Button( m2,bg='white',text="Submit",width=20,height=1,borderwidth=3,highlightbackground="black",
                    relief=SOLID,command=getdata4 )
    butt1.grid( row=4,column=0,pady=15,padx=1 )
    r.mainloop()

# analyze top tweets

def show6():
    def getE1():
        return E1.get()

    def getdata5():
        getE1()
        search2 = getE1()


        list=[]

        stop_words=set(stopwords.words('english'))


        for tweet in tweepy.Cursor( api.search,q=search2,lang="en" ).items(10):

            print( tweet.created_at,tweet.text )
            text=tweet.text
            list1=text.join(re.findall("[a-z][^A-Z]*",text)).split()
            list1=re.sub("http\S+\s"," ",text).split()
            list1 = re.sub( "RT|cc"," ",text ).split()
            list1 = re.sub( "#\S+"," ",text ).split()
            list1 = re.sub( "@\S+"," ",text).split()
            list1 = re.sub( "[%s]" % re.escape(":!")," ",text).split()
            list1= re.sub( "\s+"," ",text).split()

            for word in list1:
                if word not in stop_words:
                    list.append(word)
        count=Counter(list).most_common(3)
        print(count)
    r = Tk()
    r.resizable( False,False )
    r.geometry( "300x300" )
    m2 = Frame( r,width=300,height=300,bg="white" )
    m2.pack( fill=BOTH,expand=1 )

    label1 = Label( m2,text="Enter the item  you want to search",width=28,height=2,font=('times',15,'italic'),
                    bg="white" )
    label1.grid( row=0,column=0,padx=0,pady=40 )
    E1 = Entry( m2,border=4 )
    E1.grid(row=1,column=0)
    butt1 = Button( m2,bg='white',text="Submit",width=20,height=1,borderwidth=3,highlightbackground="black",
                    relief=SOLID,command=getdata5 )
    butt1.grid( row=4,column=0,pady=15,padx=1 )
    r.mainloop()



#compare the tweets

def show7():
    def getE1():
        return E1.get()

    def getE2():
        return E2.get()

    def getE3():
        return E3.get()

    def getE4():
        return E4.get()

    def getdata6():
        getE1()
        first = getE1()
        getE2()
        second= getE2()
        getE3()
        words1= getE3()
        getE4()
        words2 = getE4()


        tweets=api.user_timeline(screen_name=first)
        tweets2=api.user_timeline(screen_name=second)
        s1=''
        s2=''
        for tweet in tweets:
            s1+=tweet.text
        print(s1.count(words1))
        for tweet in tweets2:
            s2+=tweet.text
        print(s2.count(words2))
    r = Tk()
    r.resizable( False,False )
    r.geometry( "500x500" )
    m2 = Frame( r,width=500,height=500,bg="white" )
    m2.pack( fill=BOTH,expand=1 )

    label1 = Label( m2,text="Enter the first user",width=45,height=2,font=('times',15,'italic'),
                    bg="white" )
    label1.grid( row=0,column=0,padx=1,pady=10 )
    E1 = Entry( m2,border=4 )
    E1.grid()
    label2 = Label( m2,text="Enter the second user",width=45,height=2,font=('times',15,'italic'),
                    bg="white" )
    label2.grid( row=2,column=0,padx=0,pady=10 )
    E2 = Entry( m2,border=4 )
    E2.grid()
    label3 = Label( m2,text="Enter the word used by first user ",width=45,height=2,font=('times',15,'italic'),
                    bg="white" )
    label3.grid( row=4,column=0,padx=0,pady=10 )
    E3 = Entry( m2,border=4 )
    E3.grid( )
    label4 = Label( m2,text="Enter the word used by second user",width=45,height=2,font=('times',15,'italic'),
                    bg="white" )
    label4.grid( row=6,column=0,padx=0,pady=10 )
    E4 = Entry( m2,border=4 )
    E4.grid()
    butt1 = Button( m2,bg='white',text="Submit",width=20,height=1,borderwidth=3,highlightbackground="black",
                    relief=SOLID,command=getdata6 )
    butt1.grid( row=8,column=0,pady=15,padx=1 )
    r.mainloop()





def view():

    ap=Tk()
    ap.resizable(False,False)
    m1 = Frame( ap,width=680,height=680,bg="white" )
    m1.pack( fill=BOTH,expand=1 )
    ap.geometry( "650x680" )



    label1= Label(m1,text="Menu",width=25,height=2,font=('times', 50, 'italic'),bg="white")
    label1.grid( row=0,column=0,padx=1,pady=1)
    butt1 = Button(m1,bg='white',text="Retrieve the tweets",width=25,height=1 ,borderwidth=3,highlightbackground="black",relief=SOLID,command=show1)
    butt1.grid(row=1,column=0,pady=15,padx=1)


    butt2 = Button(m1,bg='white',text="Sentiment Analysis",width=25,height=1,borderwidth=3,highlightbackground="black",relief=SOLID,command=show2)
    butt2.grid(row=2,column=0,pady=15)

    butt3 = Button(m1,bg='white',text="Count the follower",width=25,height=1,borderwidth=3,highlightbackground="black",relief=SOLID,command=show3 )
    butt3.grid( row=3,column=0,pady=15 )

    butt4 = Button(m1,bg='white',text="Tweet a message",width=25,height=1 ,borderwidth=3,highlightbackground="black",relief=SOLID,command=show4)
    butt4.grid( row=4,column=0,pady=15 )

    butt5 = Button(m1,bg='white',text="Location,Language,Timezone",width=25,height=1,borderwidth=3,highlightbackground="black",relief=SOLID,command=show5)
    butt5.grid( row=5,column=0,pady=15 )

    butt6 = Button(m1,bg='white',text="Analyze top tweets",width=25,height=1,borderwidth=3,highlightbackground="black",relief=SOLID,command=show6 )
    butt6.grid( row=6,column=0,pady=15 )

    butt7= Button( m1,bg='white',text="Compare tweets",width=25,height=1,borderwidth=3,highlightbackground="black",relief=SOLID,command=show7 )
    butt7.grid( row=7,column=0,pady=15 )

    ap.mainloop()





master=Tk()
master.resizable(False,False)
m1=Frame(master,width=500,height=500 ,bg="white")
m1.pack(fill=BOTH,expand=1)
master.geometry("650x680")


image = Image.open('twitter-117595_960_720 (1).png')
photo_image = ImageTk.PhotoImage(image)
label = Label(m1, image = photo_image)
label.image=image
label.grid(row=0,column=0,padx=1,pady=10,columnspan=2,rowspan=1)

button =Button(m1,text="Twitter API",width=15,height=2,font=('times', 40, 'italic'),bg="white",borderwidth=3,highlightbackground="black",relief=SOLID,command=view)
button.grid( row=0,column=0,padx=1,pady=1)
master.mainloop()




