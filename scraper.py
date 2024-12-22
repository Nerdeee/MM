import os
import requests
import praw # python reddit API wrapper
import os
from dotenv import load_dotenv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re 

# look at differences between requests and beautifulsoup and which one would be best for my needs

# nltk.download('vader_lexicon') # uncomment this line to get access to the vader_lexicon

sia = SentimentIntensityAnalyzer()

class RequestHandler:
    def __init__(self):
        return

def sentimentTest(text):
        score = sia.polarity_scores(text)
        print(score)

def main():
    custom_lexicon = {
        "balding": -1.0,
        "you're balding": -2.0,
        "your balding": -2.0,
        "ur balding": -2.0,
        "yr balding": -2.0,
        "fin": -3.0,
        "thin": -2.0,
        "thinning": -2.0,
    }

    sia.lexicon.update(custom_lexicon)

    regular_expressions = [re.compile("normal"), re.compile("maturing"), re.compile("rip"), re.compile("my condolences"),
                           re.compile("and im not balding"), re.compile("i dont see"), re.compile("has a natural"),
                           re.compile("yes"), re.compile("no"), re.compile("nah"), re.compile("you're good"), re.compile("ur good"),
                           re.compile("nope"), re.compile("a natural"), re.compile("balding"), re.compile("you're balding"),
                           re.compile("your balding"), re.compile("ur balding"), re.compile("yr balding"), re.compile("fin"),
                           re.compile("thin"), re.compile("thinning")]

    test_cases = [
        "looks like you're balding",
        "you need to start fin",
        "id start taking fin ASAP",
        "looks like you're not balding",
        "don't worry, it's just a cowlick",
        "Nope. You have medium - low density but the hair strands individually are very thick. Its normal for cowlick/ crown area to be bit less in density. The baby hairs near the temple area are also gonna thin out slowly in the coming years, giving you a mature hairline. Quite normal.",
    ]

    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        password=os.getenv('PASSWORD'),
        user_agent=os.getenv('USER_AGENT'),
        username=os.getenv('USERNAME'),
    )

    # Test area
    """ for key in custom_lexicon.keys():
        print(f'{key}: {sia.lexicon.get(key)}')
    print()
    for test in test_cases:
        sentimentTest(test) """
    print()
    for sentence in test_cases:
        print(f'Sentence: {sentence}')
        for regex in regular_expressions:
            print(f'{regex} --- {regex.search(sentence)}')
                
if __name__ == "__main__":
    main()