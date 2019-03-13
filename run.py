from Sentimental import Sentimental


lang = "en"


if __name__ == '__main__':

    searchTerm, noOfSearchTerms = Sentimental.get_inputs()

    print("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " Tweets.")

    sentimental = Sentimental(searchTerm, noOfSearchTerms, lang)
    sentimental.analyze_polarity()
    sentimental.graph_pie()
    polarity = sentimental.get_polarity()

    if polarity == 0:
        print("Neutral")
    elif polarity < 0.00:
        print("Negative")
    elif polarity > 0.00:
        print("Positive")
