import os
import sys
import re
import praw
import openai
from dotenv import load_dotenv
from datetime import datetime
import logging

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.base_url = "https://openrouter.ai/api/v1/"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Validate input
if len(sys.argv) != 2:
    logger.error('Usage: python main.py <reddit_profile_url>')
    sys.exit(1)

profile_url = sys.argv[1]

# Extract username from URL
def extract_username(url):
    match = re.search(r'reddit\.com/user/([A-Za-z0-9_\-]+)', url)
    if match:
        return match.group(1)
    else:
        logger.error('Invalid Reddit profile URL.')
        sys.exit(1)

username = extract_username(profile_url)

# Initialize Reddit API
try:
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
    )
except Exception as e:
    logger.error(f"Failed to initialize Reddit API: {e}")
    sys.exit(1)

# Fetch user posts and comments
def fetch_user_data(username):
    user = reddit.redditor(username)
    posts = []
    comments = []

    try:
        for submission in user.submissions.new(limit=100):
            posts.append({
                'type': 'post',
                'title': submission.title,
                'body': submission.selftext or 'N/A',
                'url': submission.url,
                'permalink': f"https://www.reddit.com{submission.permalink}",
                'created_utc': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'subreddit': str(submission.subreddit)
            })
    except Exception as e:
        logger.warning(f"Error fetching posts for {username}: {e}")

    try:
        for comment in user.comments.new(limit=100):
            comments.append({
                'type': 'comment',
                'body': comment.body,
                'permalink': f"https://www.reddit.com{comment.permalink}",
                'created_utc': datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'subreddit': str(comment.subreddit)
            })
    except Exception as e:
        logger.warning(f"Error fetching comments for {username}: {e}")

    logger.info(f"Fetched {len(posts)} posts and {len(comments)} comments for user {username}.")
    return posts, comments

# Generate user Persona using OpenRouter
def generate_persona(posts, comments, username):
    # Combine posts and comments into a single text for analysis
    content = []
    for post in posts:
        content.append(f"Post in r/{post['subreddit']}: {post['title']} - {post['body']} (URL: {post['permalink']})")
    for comment in comments:
        content.append(f"Comment in r/{comment['subreddit']}: {comment['body']} (URL: {comment['permalink']})")

    content_text = "\n".join(content)

    if not content_text:
        logger.warning("No content to analyze.")
        return "No sufficient data to generate persona."

    # OpenRouter prompt for persona generation
    prompt = f"""
    Analyze the following Reddit posts and comments by user '{username}' to create a user persona.
    The persona should include characteristics such as interests, personality traits, hobbies, and demographics (if inferable).
    For each characteristic, provide a brief explanation and cite the specific post or comment (with its URL) used to infer it.
    Format the output as follows:

    ## User Persona: {username}

    ### Characteristic 1: [Description]
    - **Explanation**: [Why this characteristic was inferred]
    - **Source**: [Post/Comment text snippet] (URL: [permalink])

    ### Characteristic 2: [Description]
    - **Explanation**: [Why this characteristic was inferred]
    - **Source**: [Post/Comment text snippet] (URL: [permalink])

    ...

    Reddit Content:
    {content_text}
    """

    try:
        response = openai.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful AI that analyzes social media data to create user personas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating persona with OpenRouter: {e}")
        return "Failed to generate persona due to API error."

# Save persona to a text file
def save_persona(persona, username):
    output_dir = "personas"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{username}_persona.txt")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(persona)
        logger.info(f"Persona saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving persona to file: {e}")

# Main execution
def main():
    posts, comments = fetch_user_data(username)
    persona = generate_persona(posts, comments, username)
    save_persona(persona, username)

if __name__ == "__main__":
    main()