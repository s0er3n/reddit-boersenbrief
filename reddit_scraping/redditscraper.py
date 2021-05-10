import time
import datetime
import praw
from dotenv import load_dotenv
import os
import json
# import pandas as pd
load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    password=os.environ.get("password"),
    user_agent=os.environ.get("user_agent"),
    username=os.environ.get("username")
)


def give_example_selftext():
    url = "https://www.reddit.com/r/mauerstrassenwetten/comments/n6vlm4/reddit_fomo_alert_report_prototyp/"

    submission = reddit.submission(url=url)

    return submission.selftext


def top10(subreddit):
    posts = []
    for post in reddit.subreddit(subreddit).top("week", limit=100):
        if post.selftext:
            posts += ("# "+post.title.strip() + "\n",
                      post.selftext)
    print(posts)
    return posts


# start = "03/05/2021"
# end = "10/05/2021"

# start_timeframe = time.mktime(
#     datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
# end_timeframe = time.mktime(
#     datetime.datetime.strptime(end, "%d/%m/%Y").timetuple())

# print(start_timeframe)

# ml_subreddit = reddit.subreddit('Wallstreetbets')
# posts = []
# for post in ml_subreddit.hot(limit=50):
#     if post.link_flair_text == 'DD' and post.upvote_ratio >= 0.750 and start_timeframe <= post.created_utc < end_timeframe:
#         print(post.created_utc)
#         print(post.url)
#         posts.append([post.title, post.score, post.id, post.url, post.num_comments,
#                      post.selftext, post.created, post.upvote_ratio, post.link_flair_text])
# posts = pd.DataFrame(posts, columns=[
#                      'title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'ratio', 'flair'])
# print(posts)


# print(top10("Wallstreetbets"))
