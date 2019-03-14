#!/usr/bin/python3
from Sentimental import Sentimental


lang = "es"


if __name__ == '__main__':

    search_term, no_of_search_terms = Sentimental.get_inputs()

    print("How people are reacting on " + search_term + " by analyzing " + str(no_of_search_terms) + " Tweets.")

    sentimental = Sentimental(search_term, no_of_search_terms, lang)
    sentimental.analyze_polarity()
    
    polarity = sentimental.get_polarity()

    if polarity == 0:
        print("Neutral")
    elif polarity < 0.00:
        print("Negative")
    elif polarity > 0.00:
        print("Positive")

    sentimental.graph_pie()
