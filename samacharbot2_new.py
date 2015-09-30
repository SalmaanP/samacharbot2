__author__ = 'salmaan'
import praw
from prawoauth2 import PrawOAuth2Mini
import os
from ignore import config
import blacklist
import smrzr
import find_other_news_sources

blockedid = []


reddit_client = praw.Reddit(user_agent="Samachar Bot for /r/india by /u/sallurocks")
oauth_helper = PrawOAuth2Mini(reddit_client, app_key=config.app_key,
                              app_secret=config.app_secret,
                              access_token=config.access_token,
                              refresh_token=config.refresh_token, scopes=config.scopes)


def get_latest_posts(subreddit):

    subreddit = reddit_client.get_subreddit(subreddit)
    return subreddit.get_new(limit=25)


def prepare(submission):
    link = submission.url
    summ_article = smrzr.Summarizer(link)
    keypoints = summ_article.keypoints
    summ = summ_article.summary
    message = "\n\n> * ".join(keypoints)
    message = "> * " + message
    message = message.replace("`", "")
    message = message.replace("#", "\#")

    # Find relevant links using google
    relevant_list = find_other_news_sources.find_other_news_sources(url=link)