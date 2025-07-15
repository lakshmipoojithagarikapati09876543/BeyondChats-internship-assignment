from dotenv import load_dotenv
import os

load_dotenv()
print("REDDIT_CLIENT_ID:", os.getenv('REDDIT_CLIENT_ID'))
print("REDDIT_CLIENT_SECRET:", os.getenv('REDDIT_CLIENT_SECRET'))
print("REDDIT_USER_AGENT:", os.getenv('REDDIT_USER_AGENT'))
print("OPENAI_API_KEY:", os.getenv('OPENAI_API_KEY'))
print("REDDIT_USERNAME:", os.getenv('REDDIT_USERNAME'))
print("REDDIT_PASSWORD:", os.getenv('REDDIT_PASSWORD'))