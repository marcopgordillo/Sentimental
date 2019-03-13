from textblob import TextBlob
from textblob.exceptions import TranslatorError, NotTranslated
import tweepy
import matplotlib.pyplot as plt
from secret import *


lang = "es"
searchTerm = ''
noOfSearchTerms = 0


def percentage(part, whole):
    return 100 * float(part)/float(whole)


def get_auth():
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    return tweepy.API(auth)


def get_inputs():
    searchTerm = input("Enter keyword/hashtag to search about: ")
    noOfSearchTerms = int(input("How many tweets to analyze: "))
    return searchTerm, noOfSearchTerms


def get_tweets(api):
    return tweepy.Cursor(api.search, q=searchTerm).items(noOfSearchTerms)


def analyze_polarity(tweets, lang):
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    for tweet in tweets:
        # print(tweet.text)

        try:
            analysis = TextBlob(tweet.text).translate(lang)
        except NotTranslated as error:
            print(error)
            pass
        except TranslatorError as error:
            print(error)
            pass
        else:
            polarity += analysis.sentiment.polarity
            if analysis.sentiment.polarity == 0:
                neutral += 1
            elif analysis.sentiment.polarity < 0.00:
                negative += 1
            elif analysis.sentiment.polarity > 0.00:
                positive += 1

    positive = percentage(positive, noOfSearchTerms)
    negative = percentage(negative, noOfSearchTerms)
    neutral = percentage(neutral, noOfSearchTerms)
    polarity = percentage(polarity, noOfSearchTerms)

    positive = format(positive, '.2f')
    negative = format(negative, '.2f')
    neutral = format(neutral, '.2f')

    return positive, neutral, negative, polarity


def graph_pie():
    labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]']
    sizes = [positive, neutral, negative]

    colors = ['yellowgreen', 'gold', 'red']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " Tweets.")

    plt.axis('equal')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    api = get_auth()
    searchTerm, noOfSearchTerms = get_inputs()
    tweets = get_tweets(api)
    positive, neutral, negative, polarity = analyze_polarity(tweets, lang)

    print("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " Tweets.")

    if polarity == 0:
        print("Neutral")
    elif polarity < 0.00:
        print("Negative")
    elif polarity > 0.00:
        print("Positive")

    graph_pie()
