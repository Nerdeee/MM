import os
import requests
import praw # python reddit API wrapper
import os
from dotenv import load_dotenv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

# look at differences between requests and beautifulsoup and which one would be best for my needs

# nltk.download('vader_lexicon') # uncomment this line to get access to the vader_lexicon

sia = SentimentIntensityAnalyzer()

class SentimentAnalysis:
    def __init__(self):
        return

class RequestHandler:
    def __init__(self):
        return

def main():
    custom_lexicon = {
        "you're balding": -1.0,
        "your balding": -1.0,
        "ur balding": -1.0,
        "yr balding": -1.0,


    }

    sia.lexicon.update(custom_lexicon)

    test_negative = "looks like you're balding"
    test_negative2 = "id start taking fin ASAP"
    test_positive = "looks like you're not balding"
    test_positive2 = "don't worry, it's just a cowlick"

    def sentimentTest(text):
        score = sia.polarity_scores(text)
        print(score)

    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        password=os.getenv('PASSWORD'),
        user_agent=os.getenv('USER_AGENT'),
        username=os.getenv('USERNAME'),
    )

    sentimentTest(test_negative)
    sentimentTest(test_negative2)
    sentimentTest(test_positive)
    sentimentTest(test_positive2)
    return

if __name__ == "__main__":
    main()