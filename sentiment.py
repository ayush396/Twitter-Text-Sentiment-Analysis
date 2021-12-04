import numpy as np
import tweepy
import pandas as pd
import re
import emoji

import os
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
nltk.download('stopwords')


from textblob import TextBlob

def subjectivity(text):
        return TextBlob(text).sentiment.subjectivity


def polarity(text):
        return TextBlob(text).sentiment.polarity

def analysis(score):
    if score<0:
        return 'Negative'
    elif score==0:
        return 'Neutral'
    else:
        return 'Positive'  

def mapped_analysis(score):
    if score<0:
        return emoji.emojize(":crying_face:")
    elif score==0:
        return emoji.emojize(":neutral_face:")
    else:
        return emoji.emojize(":grinning_face_with_big_eyes:")

def cleanText(text):
    text=re.sub(r',','',text)
    text=re.sub(r'\n',' ',text)
    return text


class Sentiment():

    def __init__(self):
        self.consumer_key='5llhsgRXcFVzrARDogczwvmMD'
        self.consumer_secret='gnbI6bfmxq7jgIt3AFGkDknqfGwmZaQCJr07ha9RRoivuNVDEw'
        self.access_token='1277991745972654081-PWk0eMUvSjoUJiVaCr6MlQQjb1y6cq'
        self.access_token_secret='6oAvj6hZmeDjq48lcvPn3pESAKQTYBMzzQue0PTW3sbO4'
        self.tweet=""

        self.pos_count=0
        self.neg_count=0
        self.neutral_count=0

        self.tweets=[]
        self.likes=[]
        self.stoplist=nltk.corpus.stopwords.words(fileids='english')
        self.tokenizer=RegexpTokenizer(r'\w+')
        self.ps=PorterStemmer()

    def getCleaned(self,text):
        text=re.sub(r'RT[\s]+','',text)
        text=text.lower()
        tokens=self.tokenizer.tokenize(text)
        #alphabets=[]
        alphabets=[word for word in tokens if word.isalpha()]
        
        new_tokens=[token for token in alphabets if token not in self.stoplist]
    
        stemmed_tokens=[self.ps.stem(tokens) for tokens in new_tokens]
    
        clean_text=" ".join(stemmed_tokens)
    
        return clean_text  

    def getSentiment(self):
        ans=self.getCleaned(self.tweet)
        polar=polarity(ans)
        sentiment=mapped_analysis(polar)
        return sentiment


    def process(self):
        #os.remove("env//static//tweet.csv")
        self.tweets.clear()
        self.likes.clear()
        self.pos_count=0
        self.neg_count=0
        self.neutral_count=0
        auth=tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        auth.set_access_token(self.access_token,self.access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)

        for i in tweepy.Cursor(api.user_timeline,id=self.fname,tweet_mode='extended').items(100):
            self.tweets.append(i.full_text)
            self.likes.append(i.favorite_count)

        df=pd.DataFrame({'Tweets':self.tweets,'likes':self.likes})
        df['newtweets']=df['Tweets'].apply(self.getCleaned)

        df['Subjectity']=df['newtweets'].apply(subjectivity)
        df['Polarity']=df['newtweets'].apply(polarity)
        final=' '.join([word for word in df['newtweets']])
        
        df['Sentiment']=df['Polarity'].apply(analysis)

        # for i in range(100):
        #     if df['Sentiment'][i]=='Negative':
        #         print(df['tweets'][i])

        df=df.drop('Subjectity',axis=1)
        df=df.drop('newtweets',axis=1)
        df=df.drop('Polarity',axis=1)
        
        df['Tweets']=df['Tweets'].apply(cleanText)

        for i in df['Sentiment']:
            if i=='Positive':
                self.pos_count=self.pos_count+1
            elif i=='Negative':
                self.neg_count=self.neg_count+1
            else:
                self.neutral_count=self.neutral_count+1


        df['Sentiment']=df['Sentiment'].map({'Positive':emoji.emojize(":grinning_face_with_big_eyes:"),'Neutral':emoji.emojize(":neutral_face:"),'Negative':emoji.emojize(":crying_face:")})
        
 
        df.to_csv('env//static//tweet.csv',index=False)
        df.drop(['Tweets','likes','Sentiment'],axis=1,inplace=True)
        
        print(self.pos_count)



