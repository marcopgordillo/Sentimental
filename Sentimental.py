from secret import *
import tweepy
from textblob import TextBlob
from textblob.exceptions import TranslatorError, NotTranslated
import matplotlib.pyplot as plt


class Sentimental:

    def __init__(self, search_term, no_of_search_terms, lang):
        self.__lang = lang
        self.__searchTerm = search_term
        self.__noOfSearchTerms = no_of_search_terms
        self.__api = self.get_auth()
        self.__positive = 0
        self.__negative = 0
        self.__neutral = 0
        self.__polarity = 0
        self.__tweets = self.get_tweets()

    @staticmethod
    def get_inputs():
        search_term = input("Enter keyword/hashtag to search about: ")
        no_of_search_terms = int(input("How many tweets to analyze: "))
        return search_term, no_of_search_terms

    @staticmethod
    def get_auth():
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        return tweepy.API(auth)

    def percentage(self, part):
        return 100 * float(part) / float(self.__noOfSearchTerms)

    def get_tweets(self):
        return tweepy.Cursor(self.__api.search, q=self.__searchTerm).items(self.__noOfSearchTerms)

    def analyze_polarity(self):

        positive = 0
        neutral = 0
        negative = 0
        polarity = 0

        for tweet in self.__tweets:
            # print(tweet.text)
            try:
                analysis = TextBlob(tweet.text).translate(self.__lang)
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

        for i in [positive, negative, neutral, polarity]:
            i = self.percentage(i)
            i = format(i, '.2f')

        self.__positive = positive
        self.__negative = negative
        self.__neutral = neutral
        self.__polarity = polarity

    def graph_pie(self):
        labels = ['Positive [' + str(self.__positive) + '%]', 'Neutral [' + str(self.__neutral) + '%]',
                  'Negative [' + str(self.__negative) + '%]']
        sizes = [self.__positive, self.__neutral, self.__negative]

        colors = ['yellowgreen', 'gold', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title("How people are reacting on " + self.__searchTerm + " by analyzing " + str(self.__noOfSearchTerms) +
                  " Tweets.")

        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def get_polarity(self):
        return self.__polarity
