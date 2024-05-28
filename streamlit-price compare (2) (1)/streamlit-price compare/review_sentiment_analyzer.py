from textblob import TextBlob
import sys

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string
# from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

nltk.downloader.download('vader_lexicon')


def percentage(part, whole):
    return 100 * float(part)/float(whole)


# pd.read_csv('review_csv/{0}_amazon.csv'.format(name))


def review_analyzer(name):
    df = pd.read_csv('review_csv/{0}_amazon.csv'.format(name))
    tweets = df['body']
    noOfTweet = len(df)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []
    for tweet in tweets:
        try:
            tweet_list.append(tweet)
            analysis = TextBlob(tweet)
            # df['body'].apply(lambda tweet: TextBlob(tweet).sentiment)
            # analysis = df['body'].apply(sentiment_calc)
            score = SentimentIntensityAnalyzer().polarity_scores(tweet)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            comp = score['compound']
            polarity += analysis.sentiment.polarity
            if neg > pos:
                negative_list.append(tweet)
                negative += 1
            elif pos > neg:
                positive_list.append(tweet)
                positive += 1
            elif pos == neg:
                neutral_list.append(tweet)
                neutral += 1
            positive = percentage(positive, noOfTweet)
            negative = percentage(negative, noOfTweet)
            neutral = percentage(neutral, noOfTweet)
            # polarity = percentage(polarity, noOfTweet)
            positive = format(positive, '.1f')
            negative = format(negative, '.1f')
            neutral = format(neutral, '.1f')
        except TypeError:
            continue

    tweet_list = pd.DataFrame(tweet_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    tot_num = len(tweet_list)
    pos_num = len(positive_list)
    neg_num = len(negative_list)
    neu_num = len(neutral_list)
    # print("total number: ", len(tweet_list))
    # print("positive number: ", len(positive_list))
    # print("negative number: ", len(negative_list))
    # print("neutral number: ", len(neutral_list))
    return (tot_num, pos_num, neg_num, neu_num)


# review_analyzer('tv')
