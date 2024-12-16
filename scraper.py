import os
import requests
import praw # python reddit API wrapper
import os
from dotenv import load_dotenv
from textblob import TextBlob

# look at differences between requests and beautifulsoup and which one would be best for my needs

class RequestHandler:
    def __init__(self):
        return

def main():
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        password=os.getenv('PASSWORD'),
        user_agent=os.getenv('USER_AGENT'),
        username=os.getenv('USERNAME'),
    )
    return

if __name__ == "__main__":
    main()