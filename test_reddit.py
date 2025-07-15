import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

try:
    subreddit = reddit.subreddit("python")
    for post in subreddit.hot(limit=1):
        print("Fetched post title:", post.title)
    print("API connection successful!")
except Exception as e:
    print(f"API connection failed: {e}")