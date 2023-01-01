import os
import pickle
import re

import nltk
import snscrape.modules.twitter as sns_twitter
import tensorflow as tf
from googletrans import Translator
from keras.models import load_model
from nltk.corpus import stopwords
from scipy.special import softmax
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

filePath = "Text_Vectorization"

stop_words = None
tokenizer = None
model = None
load_text_Vectorizer_layer = None
load_text_Vectorizer_Model = None
stored_Model = None
labels = ['Negative', 'Neutral', 'Positive']
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
# Set the local path where the file will be downloaded
local_path = "/"

# Check if the file already exists in the local directory
if not os.path.exists("roberta_model.pkl"):
    # Download the file from the URL
    print("file doesnot exit in dir")
    model = TFAutoModelForSequenceClassification.from_pretrained(roberta, from_pt=True)

if load_text_Vectorizer_Model is None and load_text_Vectorizer_layer is None:
    load_text_Vectorizer_Model = tf.keras.models.load_model(filePath)
    load_text_Vectorizer_layer = load_text_Vectorizer_Model.layers[0]

if stored_Model is None:
    stored_Model = load_model('ManuallyTrainedModel.h5')

if stop_words is None:
    nltk.download('stopwords')
    stop_words = set(stopwords.words("english"))

# pickle.dump(model, open('model.pkl', 'wb'))
if tokenizer is None:
    tokenizer = AutoTokenizer.from_pretrained(roberta)

if model is None:
    print("loading model from pickle...")
    model = pickle.load(open("roberta_model.pkl", "rb"))

# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from scipy.special import softmax
# # Creating object of translator
translator = Translator(service_urls=['translate.googleapis.com'])

query1 = "Bitcoin"


# limit = 20  # initial limit


def get_translated_tweets(query, from_date, to_date, limit):
    tweets_list = []
    i = 0
    # print(query + " since:" + from_date + " until:" + to_date + "limit" + limit)
    for tweet in sns_twitter.TwitterSearchScraper(query + " since:" + from_date + " until:" + to_date).get_items():
        if (int(limit) == i):
            break
        else:
            #   attributes_container.append([tweet.date, tweet.likeCount, tweet.sourceLabel, tweet.content])'
            # print("tweet" + str(tweet) + "   ::" + str(len(tweets_list)))
            tweet_dic = {
                "tweet": remove_stop_words_and_punctuations(translator.translate(tweet.content).text),
                "date": str(tweet.date.date())
            }
        i = i + 1
        tweets_list.append(tweet_dic)
    return tweets_list


def remove_stop_words_and_punctuations(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = [w for w in text.split() if w not in stop_words]
    return " ".join(text)


def analyze_tweets_pre_trained_model(tweets, model_selected):
    positive = 0
    negative = 0
    neutral = 0
    if model_selected == '1':
        for tweet in tweets:
            # print(cleanedText)
            textString = str(tweet["tweet"])
            # sentiment analysis
            encoded_tweet = tokenizer(textString, return_tensors='pt')
            # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
            output = model(**encoded_tweet)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)

            negScore = scores[0]
            neuScore = scores[1]
            posScore = scores[2]

            if max(posScore, neuScore, negScore) == posScore:
                positive += 1
            elif max(posScore, neuScore, negScore) == neuScore:
                neutral += 1
            elif max(posScore, neuScore, negScore) == negScore:
                negative += 1

            """# Searched KeyWord is 'Machine Learning'"""

            # print("searched keyword is : ", , "\n")
            print("Number of positive Tweets are  :  ", positive)
            print("Number of Negative Tweets are  :  ", negative)
            print("Number of Neutral Tweets are   :  ", neutral)
    else:
        for tweet in tweets:
            vector = load_text_Vectorizer_layer([tweet["tweet"]], )
            result = stored_Model.predict(vector, verbose=0)

            if result[0][0] >= 0.5:
                positive += 1
            else:
                negative += 1

    return {"positive": positive, "negative": negative, "neutral": neutral}
