"""
Fetch Reddit thread comments and save as JSON for ThreadQA
"""
import praw
import json

# Fill in your Reddit API credentials
reddit = praw.Reddit(
    client_id='YOUR_ID',
    client_secret='YOUR_SECRET',
    user_agent='ThreadQA'
)

thread_url = input("Enter Reddit thread URL: ")
submission = reddit.submission(url=thread_url)

comments = []
for comment in submission.comments.list():
    if hasattr(comment, 'body'):
        comments.append({
            "timestamp": str(comment.created_utc),
            "author": str(comment.author),
            "message": comment.body
        })

out_path = "data/thread_from_api.json"
with open(out_path, "w") as f:
    json.dump(comments, f, indent=2)
print(f"Saved {len(comments)} comments to {out_path}")
