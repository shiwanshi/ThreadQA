"""
Fetch all posts and comments from a subreddit and save as JSON for ThreadQA
"""
import praw
import json

# Fill in your Reddit API credentials
reddit = praw.Reddit(
    client_id='YOUR_ID',
    client_secret='YOUR_SECRET',
    user_agent='ThreadQA'
)

subreddit_name = input("Enter subreddit name (e.g., Python): ")
limit = int(input("How many posts to fetch? (e.g., 100): "))

all_items = []
subreddit = reddit.subreddit(subreddit_name)
for submission in subreddit.new(limit=limit):
    all_items.append({
        "timestamp": str(submission.created_utc),
        "author": str(submission.author),
        "message": submission.title + "\n" + submission.selftext
    })
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        if hasattr(comment, 'body'):
            all_items.append({
                "timestamp": str(comment.created_utc),
                "author": str(comment.author),
                "message": comment.body
            })

out_path = "data/subreddit_dump.json"
with open(out_path, "w") as f:
    json.dump(all_items, f, indent=2)
print(f"Saved {len(all_items)} items to {out_path}")
