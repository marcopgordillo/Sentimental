from secret import *
import tweepy
from textblob import TextBlob
from textblob.exceptions import TranslatorError, NotTranslated
import matplotlib.pyplot as plt


class Sentimental:

    def __init__(self, search_term, no_of_search_terms, lang):
        self.lang = lang
        self.searchTerm = search_term
        self.noOfSearchTerms = no_of_search_terms
        self.api = self.get_auth()
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.polarity = 0
        self.tweets = self.get_tweets()

    def percentage(self, part):
        return 100 * float(part) / float(self.noOfSearchTerms)

    @staticmethod
    def get_auth():
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        return tweepy.API(auth)

    def get_tweets(self):
        return tweepy.Cursor(self.api.search, q=self.searchTerm).items(self.noOfSearchTerms)

    def analyze_polarity(self):

        for tweet in self.tweets:
            # print(tweet.text)
            positive = 0
            neutral = 0
            negative = 0
            polarity = 0

            try:
                analysis = TextBlob(tweet.text).translate(self.lang)
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

        self.positive = positive
        self.negative = negative
        self.neutral = neutral
        self.polarity = polarity

    def graph_pie(self):
        labels = ['Positive [' + str(self.positive) + '%]', 'Neutral [' + str(self.neutral) + '%]',
                  'Negative [' + str(self.negative) + '%]']
        sizes = [self.positive, self.neutral, self.negative]

        colors = ['yellowgreen', 'gold', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title("How people are reacting on " + self.searchTerm + " by analyzing " + str(self.noOfSearchTerms) +
                  " Tweets.")

        plt.axis('equal')
        plt.tight_layout()
        plt.show()
