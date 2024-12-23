import os
import requests
import praw # python reddit API wrapper
import os
from dotenv import load_dotenv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from praw.models import MoreComments 

# look at differences between requests and beautifulsoup and which one would be best for my needs

# nltk.download('vader_lexicon') # uncomment this line to get access to the vader_lexicon

sia = SentimentIntensityAnalyzer()

class RedditAPIHandler:
    def __init__(self, praw_obj, subreddit_name):
        self.reddit_obj = praw_obj
        self.subreddit_obj = subreddit_name
        self.sentiment_array = []
    def getSubreddit(self):
        return "Subreddit name: " + self.subreddit_obj.display_name
    def getTitles(self, query_string, batches):
        reddit = self.reddit_obj
        subreddit = self.subreddit_obj
        search_results = subreddit.search(query_string, limit=1000)
        print("\n---------------------- OP Titles ----------------------\n")
        test = 0
        test2 = 0
        for posts in search_results:
            if query_string in posts.title:
                ex = posts.url.split("/")
                print(f'Post title: {posts.title} Post URL: {posts.url}')
                if len(ex) == 5: # gallery / OP ID is in URL
                    test += 1

                else:   # means that the link is an image link and more operations need to be performed to get the OP info
                    test2 += 1
        print('number of gallery links', test)
        print('number of image links', test2)

        # testing
        gallery_submission = reddit.submission(url="https://www.reddit.com/gallery/1ahusip")
        print(f'Gallery submission title: {gallery_submission.title}\n')
        print('\n\n----Comments----\n')
        for i, c in enumerate(gallery_submission.comments.list()):
            if i > 4:
                break
            if isinstance(c, MoreComments):
                continue
            else:
                print(f'comment {i} : {c.body}')
        print("--------------------------------------------------")
        submission = reddit.subreddit("malehairadvice").search(f"url:https://i.redd.it/dmlnq0fx1wq91.jpg", limit=1)
        for post in submission:
            print(f"Title: {post.title}")
            print(f"Author: {post.author}")
            print(f"Submission URL: {post.url}")
            print(f"Selftext: {post.selftext}")  # If there's text in the post
            print(f"Number of comments: {post.num_comments}")
            """ for i, comment in enumerate(post.comments.list()):
                if isinstance(comment, MoreComments):
                    continue
                if comment.body == "[deleted]" or comment.body == "\n":
                    continue
                print(f'{i}th comment: {comment.body}') """
    def sentimentTest(self, text_array, pos_regexs, neg_regexs): # text_array will contain an array of comments per OP
            # see the number of times a word from each category appears and then whichever onehas a grater number, wins. If they tie, defauly to balding class
            original_post_sentiment = ""
            result_array = []
            for comment in text_array:
                for text in comment:
                    pos_sentiment = re.search(text, pos_regexs)
                    neg_sentiment = re.search(text, neg_regexs)
                    if neg_sentiment >= pos_sentiment:
                        result_array.append("negative")
                    else:
                        result_array.append("positive")
            original_post_sentiment = "negative" if result_array.count("negative") >= result_array.count("positive") else "positive"
            self.sentiment_array.append(original_post_sentiment)
            return
                

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

    query_string = "balding"

    comment_regular_expressions = [re.compile("normal"), re.compile("maturing"), re.compile("^rip"), re.compile("my condolences"),
                           re.compile("and im not balding"), re.compile("dont see"), re.compile("a natural"),
                           re.compile("yes"), re.compile("no"), re.compile("nah"), re.compile("you're good"), re.compile("ur good"),
                           re.compile("nope"), re.compile("balding"), re.compile("you're balding"),
                           re.compile("your balding"), re.compile("ur balding"), re.compile("yr balding"), re.compile("fin"),
                           re.compile("thin"), re.compile("thinning"), re.compile("min"), re.compile("shave"), re.compile("embrace"), re.compile("meds")]

    negative_regexs = [re.compile("maturing"), re.compile("^rip"), re.compile("my condolences"), re.compile("yes"), re.compile("you're balding"), re.compile("balding"),
                       re.compile("your balding"), re.compile("ur balding"), re.compile("yr balding"), re.compile("fin"), re.compile("thin"), re.compile("thinning"),
                       re.compile("min"), re.compile("shave"), re.compile("embrace"), re.compile("meds"), re.compile("dutasteride"), re.compile("isn't working"),
                       re.compile("isnt working")]

    positive_regexs = [re.compile("normal"), re.compile("and im not balding"), re.compile("dont see"), re.compile("a natural"), re.compile("no"), re.compile("nah"),
                       re.compile("you're good"), re.compile("ur good"), re.compile("nope")]

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
        user_agent=os.getenv('USER_AGENT'),
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
        for regex in comment_regular_expressions:
            print(f'{regex} --- {regex.search(sentence)}')
    subreddit = reddit.subreddit("malehairadvice")
    batches = 1
    redditAPIHandler = RedditAPIHandler(reddit, subreddit)
    print(redditAPIHandler.getSubreddit())
    redditAPIHandler.getTitles(query_string, batches)               
if __name__ == "__main__":
    main()